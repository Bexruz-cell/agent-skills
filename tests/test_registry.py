"""Tests for the agentic stack registry and skill validation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_registry_exists():
    assert (ROOT / "references" / "awesome_agentic_stack.json").exists()


def test_registry_has_exactly_50():
    reg = json.loads((ROOT / "references" / "awesome_agentic_stack.json").read_text())
    assert len(reg["repositories"]) == 50
    assert reg["version"] == "1.4.0"


def test_unique_ids_and_urls():
    reg = json.loads((ROOT / "references" / "awesome_agentic_stack.json").read_text())
    ids = [r["id"] for r in reg["repositories"]]
    urls = [r["url"] for r in reg["repositories"]]
    assert len(ids) == len(set(ids))
    assert len(urls) == len(set(urls))


def test_all_reference_files_exist():
    reg = json.loads((ROOT / "references" / "awesome_agentic_stack.json").read_text())
    for r in reg["repositories"]:
        path = ROOT / "references" / r["reference_file"]
        assert path.exists(), f"Missing {r['reference_file']}"


def test_skill_frontmatter():
    skills = ROOT / "skills"
    for d in skills.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            text = (d / "SKILL.md").read_text()
            assert text.startswith("---"), f"{d.name} missing frontmatter"
            assert "name:" in text
            assert "description:" in text


def test_validator_passes():
    from agent_skills.validate import main
    assert main() == 0


def test_index_exists():
    assert (ROOT / "references" / "INDEX.md").exists()


def test_repositories_dir_count():
    files = list((ROOT / "references" / "repositories").glob("*.md"))
    assert len(files) == 50
