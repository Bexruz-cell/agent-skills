"""Tests for the agentic stack registry and skill validation."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load_registry():
    return json.loads((ROOT / "references" / "awesome_agentic_stack.json").read_text(encoding="utf-8"))


def test_registry_exists():
    assert (ROOT / "references" / "awesome_agentic_stack.json").exists()


def test_exactly_50_repositories():
    reg = _load_registry()
    assert len(reg["repositories"]) == 50
    assert reg["version"] == "1.4.0"


def test_unique_repository_ids():
    reg = _load_registry()
    ids = [r["id"] for r in reg["repositories"]]
    assert len(ids) == 50
    assert len(set(ids)) == 50


def test_unique_repository_urls():
    reg = _load_registry()
    urls = [r["url"] for r in reg["repositories"]]
    assert len(urls) == 50
    assert len(set(urls)) == 50


def test_no_duplicate_repositories():
    reg = _load_registry()
    names = [r["repository"] for r in reg["repositories"]]
    assert len(names) == 50
    assert len(set(names)) == 50


def test_reference_files_exist():
    reg = _load_registry()
    for r in reg["repositories"]:
        path = ROOT / "references" / r["reference_file"]
        assert path.exists(), f"Missing {r['reference_file']}"
        assert path.stat().st_size > 50, f"Empty/too small: {r['reference_file']}"


def test_no_broken_references():
    reg = _load_registry()
    broken = [
        r["reference_file"]
        for r in reg["repositories"]
        if not (ROOT / "references" / r["reference_file"]).exists()
    ]
    assert broken == []


def test_registry_json_valid():
    reg = _load_registry()
    required = {"id", "name", "repository", "url", "category", "reference_file"}
    for r in reg["repositories"]:
        missing = required - set(r.keys())
        assert not missing, f"{r.get('id')}: missing {missing}"
        assert r["url"].startswith("https://github.com/")
        assert r["reference_file"].startswith("repositories/")


def test_markdown_matches_json():
    reg = _load_registry()
    md = (ROOT / "references" / "awesome_agentic_stack.md").read_text(encoding="utf-8")
    jrepos = {r["repository"] for r in reg["repositories"]}
    mrepos = set(re.findall(r"\*\*Repository\*\*: `([^`]+)`", md))
    assert jrepos == mrepos, f"j-only={sorted(jrepos - mrepos)[:5]} m-only={sorted(mrepos - jrepos)[:5]}"
    for r in reg["repositories"]:
        assert r["url"] in md, f"URL missing in MD: {r['url']}"


def test_registry_documents_are_synchronized():
    reg = _load_registry()
    idx = (ROOT / "references" / "INDEX.md").read_text(encoding="utf-8")
    for r in reg["repositories"]:
        assert f"`{r['id']}`" in idx, f"INDEX missing id {r['id']}"


def test_skill_frontmatter():
    skills = ROOT / "skills"
    found = 0
    for d in skills.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            found += 1
            text = (d / "SKILL.md").read_text(encoding="utf-8")
            assert text.startswith("---"), f"{d.name} missing frontmatter"
            assert "name:" in text
            assert "description:" in text
    assert found >= 2


def test_context_optimizer():
    path = ROOT / "skills" / "context-optimizer" / "SKILL.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8").lower()
    assert "name:" in text
    assert "description:" in text
    assert any(x in text for x in ("rg", "grep"))
    assert "context" in text


def test_production_hardening():
    base = ROOT / "skills" / "production-hardening"
    assert (base / "SKILL.md").exists()
    assert (base / "scripts" / "hardening_audit.py").exists()


def test_repositories_dir_count():
    files = list((ROOT / "references" / "repositories").glob("*.md"))
    assert len(files) == 50


def test_index_exists():
    assert (ROOT / "references" / "INDEX.md").exists()


def test_validator_acceptance():
    from agent_skills.validate import main

    # Must not inherit pytest sys.argv; pass explicit args
    assert main(["--skip-heavy"]) == 0


def test_validator_json_output():
    from agent_skills.validate import run_all

    payload = run_all(include_heavy=False)
    assert payload["accepted"] is True
    assert payload["status"] == "accepted"
    assert payload["version"] == "1.4.0"
    assert payload["registry"]["repositories"] == 50
    assert payload["registry"]["broken"] == 0


def test_validator_rejects_invalid_registry(tmp_path):
    """Negative test: validator must reject a broken registry (not hardcoded pass)."""
    from agent_skills import validate as v

    # Backup and break registry
    reg_path = ROOT / "references" / "awesome_agentic_stack.json"
    backup = reg_path.read_text(encoding="utf-8")
    try:
        broken = json.loads(backup)
        # Introduce duplicate ID
        broken["repositories"][0]["id"] = broken["repositories"][1]["id"]
        reg_path.write_text(json.dumps(broken), encoding="utf-8")
        payload = v.run_all(include_heavy=False)
        assert payload["accepted"] is False
        assert payload["status"] == "rejected"
        assert payload["checks"]["registry"]["status"] == "fail"
    finally:
        reg_path.write_text(backup, encoding="utf-8")


def test_validator_passes():
    """Alias kept for CI/docs compatibility; uses --skip-heavy to avoid argv clash."""
    from agent_skills.validate import main

    assert main(["--skip-heavy"]) == 0
