#!/usr/bin/env python3
"""
Production Hardening Audit Script
Performs secret scanning (regex + Shannon entropy), AST-based checks,
and emits a structured JSON report.
Exit codes: 0 = clean / only low issues, 1 = critical or high findings.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

DEFAULT_CONFIG = {
    "ignore_paths": [
        ".git/",
        "node_modules/",
        "venv/",
        ".venv/",
        "dist/",
        "build/",
        "__pycache__/",
        ".mypy_cache/",
        ".pytest_cache/",
        "coverage/",
        "tests/",
        "test/",
    ],
    "secret_patterns": [
        r"AKIA[0-9A-Z]{16}",
        r"-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----",
        r"ghp_[A-Za-z0-9]{36}",
        r"xox[baprs]-[0-9A-Za-z\-]{10,}",
        r"sk_live_[0-9a-zA-Z]{24,}",
        r"sk_test_[0-9a-zA-Z]{24,}",
    ],
    "entropy_threshold": 4.5,
    "min_secret_length": 20,
    "max_file_size_bytes": 1_048_576,
    "fail_on_severity": ["CRITICAL", "HIGH"],
    "python_extensions": [".py"],
    "node_extensions": [".js", ".ts", ".mjs", ".cjs"],
}

HTTP_CLIENT_INDICATORS: Set[str] = {
    "requests",
    "session",
    "client",
    "http",
    "aiohttp",
    "httpx",
    "urllib",
    "urllib3",
    "http_client",
    "api_client",
    "rest",
    "httpclient",
}


def shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    freq: Dict[str, int] = defaultdict(int)
    for ch in data:
        freq[ch] += 1
    length = len(data)
    return -sum((c / length) * math.log2(c / length) for c in freq.values())


def should_ignore(path: Path, ignore_paths: List[str]) -> bool:
    path_str = str(path).replace("\\", "/")
    for ign in ignore_paths:
        if ign.endswith("/") and f"/{ign}" in f"/{path_str}/":
            return True
        if path_str.endswith(ign) or f"/{ign}" in f"/{path_str}":
            return True
    name = path.name
    if name.startswith("test_") or name.endswith("_test.py"):
        return True
    return False


def scan_file_for_secrets(
    path: Path,
    patterns: List[re.Pattern],
    entropy_threshold: float,
    min_length: int,
    max_size: int,
) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    try:
        if path.stat().st_size > max_size:
            return findings
        text = path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeError):
        return findings

    lines = text.splitlines()
    for lineno, line in enumerate(lines, 1):
        for pat in patterns:
            for match in pat.finditer(line):
                secret = match.group(0)
                findings.append(
                    {
                        "severity": "CRITICAL",
                        "rule": "hardcoded-secret-regex",
                        "file": str(path),
                        "line": lineno,
                        "fingerprint": (
                            secret[:6] + "…" + secret[-4:]
                            if len(secret) > 12
                            else "***"
                        ),
                        "description": f"Matched secret pattern: {pat.pattern}",
                        "recommendation": (
                            "Move secret to environment variable or secret manager "
                            "and rotate it."
                        ),
                    }
                )

        for token in re.findall(r"[A-Za-z0-9/\+=_\-]{20,}", line):
            if len(token) < min_length:
                continue
            ent = shannon_entropy(token)
            if ent >= entropy_threshold:
                findings.append(
                    {
                        "severity": "HIGH",
                        "rule": "high-entropy-string",
                        "file": str(path),
                        "line": lineno,
                        "fingerprint": token[:6] + "…" + token[-4:],
                        "entropy": round(ent, 2),
                        "description": f"High-entropy string (entropy={ent:.2f})",
                        "recommendation": (
                            "Verify whether this is a secret. If yes, move to "
                            "env/secret store."
                        ),
                    }
                )
    return findings


def _get_attribute_chain(node: ast.AST) -> List[str]:
    parts: List[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    parts.reverse()
    return parts


def _is_http_client_call(func: ast.AST) -> bool:
    if not isinstance(func, ast.Attribute):
        return False

    method = func.attr
    if method not in {"get", "post", "put", "delete", "request", "head", "patch"}:
        return False

    chain = _get_attribute_chain(func)
    if not chain:
        return False

    for part in chain[:-1]:
        if part.lower() in HTTP_CLIENT_INDICATORS:
            return True
    return False


def ast_check_python(path: Path) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    try:
        source = path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as e:
        findings.append(
            {
                "severity": "HIGH",
                "rule": "syntax-error",
                "file": str(path),
                "line": e.lineno or 0,
                "description": f"Syntax error: {e.msg}",
                "recommendation": "Fix syntax before deployment.",
            }
        )
        return findings
    except Exception:
        return findings

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        func = node.func
        if not _is_http_client_call(func):
            continue

        has_timeout = any(
            isinstance(kw, ast.keyword) and kw.arg == "timeout"
            for kw in node.keywords
        )
        if not has_timeout:
            method = func.attr if isinstance(func, ast.Attribute) else "?"
            findings.append(
                {
                    "severity": "MEDIUM",
                    "rule": "missing-http-timeout",
                    "file": str(path),
                    "line": getattr(node, "lineno", 0),
                    "description": f"HTTP call '{method}' without explicit timeout",
                    "recommendation": "Add timeout=(connect, read) argument.",
                }
            )
    return findings


def load_config(config_path: Optional[str]) -> Dict[str, Any]:
    cfg = DEFAULT_CONFIG.copy()
    if config_path and Path(config_path).is_file():
        with open(config_path, encoding="utf-8") as f:
            user_cfg = json.load(f)
        cfg.update(user_cfg)
    return cfg


def collect_files(
    root: Path, extensions: List[str], ignore_paths: List[str]
) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d
            for d in dirnames
            if not should_ignore(Path(dirpath) / d, ignore_paths)
        ]
        for name in filenames:
            p = Path(dirpath) / name
            if should_ignore(p, ignore_paths):
                continue
            if any(name.endswith(ext) for ext in extensions):
                files.append(p)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Production Hardening Audit")
    parser.add_argument(
        "root_pos", nargs="?", default=None, help="Repository root (positional)"
    )
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--config", default=None, help="Path to audit_config.json")
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON only"
    )
    args = parser.parse_args()

    root_target = args.root_pos if args.root_pos is not None else args.root
    root = Path(root_target).resolve()
    cfg = load_config(args.config)

    patterns = [re.compile(p) for p in cfg["secret_patterns"]]
    extensions = cfg.get("python_extensions", [".py"]) + cfg.get(
        "node_extensions", [".js", ".ts"]
    )

    files = collect_files(root, extensions, cfg["ignore_paths"])
    all_findings: List[Dict[str, Any]] = []

    for path in files:
        all_findings.extend(
            scan_file_for_secrets(
                path,
                patterns,
                cfg["entropy_threshold"],
                cfg["min_secret_length"],
                cfg["max_file_size_bytes"],
            )
        )
        if path.suffix == ".py":
            all_findings.extend(ast_check_python(path))

    counts: Dict[str, int] = defaultdict(int)
    for f in all_findings:
        counts[f["severity"]] += 1

    report = {
        "status": (
            "FAILED"
            if any(s in counts for s in cfg["fail_on_severity"])
            else "PASSED"
        ),
        "summary": {
            "critical": counts["CRITICAL"],
            "high": counts["HIGH"],
            "medium": counts["MEDIUM"],
            "low": counts["LOW"],
            "files_scanned": len(files),
        },
        "findings": all_findings,
    }

    if args.json:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print(f"Status: {report['status']}")
        print(f"Files scanned: {report['summary']['files_scanned']}")
        print(
            f"Critical: {report['summary']['critical']}  "
            f"High: {report['summary']['high']}  "
            f"Medium: {report['summary']['medium']}  "
            f"Low: {report['summary']['low']}"
        )
        if all_findings:
            print("\nFindings:")
            for f in all_findings:
                print(
                    f"  [{f['severity']}] {f['file']}:{f.get('line', '?')} "
                    f"— {f['description']}"
                )

    if report["status"] == "FAILED":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
