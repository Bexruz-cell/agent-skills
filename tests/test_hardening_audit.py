#!/usr/bin/env python3
"""
Unit tests for production-hardening audit script.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

# Make the script importable
SCRIPT_DIR = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "production-hardening"
    / "scripts"
)
sys.path.insert(0, str(SCRIPT_DIR))

from hardening_audit import (  # noqa: E402
    ast_check_python,
    scan_file_for_secrets,
    shannon_entropy,
)
import re


# ---------------------------------------------------------------------------
# Shannon entropy
# ---------------------------------------------------------------------------

def test_shannon_entropy_empty():
    assert shannon_entropy("") == 0.0


def test_shannon_entropy_low():
    # ordinary English text → low entropy
    text = "hello world this is a normal sentence"
    ent = shannon_entropy(text)
    assert ent < 4.0


def test_shannon_entropy_high():
    # random-looking token
    token = "aB3xY9kL2mN8pQ5rT1vW7zC4"
    ent = shannon_entropy(token)
    assert ent >= 4.0


# ---------------------------------------------------------------------------
# Secret regex scanner
# ---------------------------------------------------------------------------

def _write_tmp(tmp_path: Path, content: str, name: str = "sample.py") -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def test_detect_aws_key(tmp_path):
    content = 'AWS_KEY = "AKIAIOSFODNN7EXAMPLE"\n'
    path = _write_tmp(tmp_path, content)
    patterns = [re.compile(r"AKIA[0-9A-Z]{16}")]
    findings = scan_file_for_secrets(path, patterns, 4.5, 20, 1_000_000)
    assert any(f["rule"] == "hardcoded-secret-regex" for f in findings)
    assert any("AKIA" in f["fingerprint"] for f in findings)


def test_detect_rsa_private_key(tmp_path):
    content = textwrap.dedent(
        """\
        KEY = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF6PZGFw...
        -----END RSA PRIVATE KEY-----'''
        """
    )
    path = _write_tmp(tmp_path, content)
    patterns = [re.compile(r"-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----")]
    findings = scan_file_for_secrets(path, patterns, 4.5, 20, 1_000_000)
    assert any(f["rule"] == "hardcoded-secret-regex" for f in findings)


def test_detect_github_token(tmp_path):
    content = 'TOKEN = "ghp_abcdefghijklmnopqrstuvwxyz0123456789"\n'
    path = _write_tmp(tmp_path, content)
    patterns = [re.compile(r"ghp_[A-Za-z0-9]{36}")]
    findings = scan_file_for_secrets(path, patterns, 4.5, 20, 1_000_000)
    assert any(f["rule"] == "hardcoded-secret-regex" for f in findings)


# ---------------------------------------------------------------------------
# AST missing-http-timeout detector
# ---------------------------------------------------------------------------

def test_requests_get_without_timeout(tmp_path):
    content = textwrap.dedent(
        """\
        import requests
        def fetch():
            return requests.get("https://example.com")
        """
    )
    path = _write_tmp(tmp_path, content)
    findings = ast_check_python(path)
    assert any(f["rule"] == "missing-http-timeout" for f in findings)
    assert any(f["severity"] == "MEDIUM" for f in findings)


def test_requests_get_with_timeout(tmp_path):
    content = textwrap.dedent(
        """\
        import requests
        def fetch():
            return requests.get("https://example.com", timeout=10)
        """
    )
    path = _write_tmp(tmp_path, content)
    findings = ast_check_python(path)
    assert not any(f["rule"] == "missing-http-timeout" for f in findings)


def test_dict_get_false_positive_protection(tmp_path):
    """dict.get / cfg.get must NOT trigger missing-http-timeout."""
    content = textwrap.dedent(
        """\
        data = {"key": "value"}
        cfg = {"timeout": 5}
        def process():
            v = data.get("key")
            t = cfg.get("timeout")
            return v, t
        """
    )
    path = _write_tmp(tmp_path, content)
    findings = ast_check_python(path)
    assert not any(f["rule"] == "missing-http-timeout" for f in findings)


def test_session_get_without_timeout(tmp_path):
    content = textwrap.dedent(
        """\
        import requests
        session = requests.Session()
        def fetch():
            return session.get("https://example.com")
        """
    )
    path = _write_tmp(tmp_path, content)
    findings = ast_check_python(path)
    assert any(f["rule"] == "missing-http-timeout" for f in findings)


# ---------------------------------------------------------------------------
# CLI integration: --json and exit codes
# ---------------------------------------------------------------------------

SCRIPT = SCRIPT_DIR / "hardening_audit.py"


def test_cli_json_clean_exit_zero(tmp_path):
    # clean project
    (tmp_path / "clean.py").write_text("print('hello')\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "--json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["status"] == "PASSED"
    assert data["summary"]["critical"] == 0
    assert data["summary"]["high"] == 0


def test_cli_json_secret_exit_one(tmp_path):
    (tmp_path / "bad.py").write_text(
        'KEY = "AKIAIOSFODNN7EXAMPLE"\n', encoding="utf-8"
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "--json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["status"] == "FAILED"
    assert data["summary"]["critical"] >= 1


def test_cli_positional_root_argument(tmp_path):
    (tmp_path / "clean.py").write_text("print('hello positional')\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path), "--json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["status"] == "PASSED"

