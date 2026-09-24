#!/usr/bin/env python3
"""Validate agent-skills repository structure, skills, and registry."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FRONTMATTER = ("name", "description")


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: Dict[str, Any] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, parts[2]


def validate_skill(skill_dir: Path) -> List[str]:
    errors: List[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"Missing SKILL.md in {skill_dir.name}")
        return errors
    text = skill_md.read_text(encoding="utf-8")
    meta, _ = parse_frontmatter(text)
    for field in REQUIRED_FRONTMATTER:
        if field not in meta or not meta[field]:
            errors.append(f"{skill_dir.name}: missing frontmatter field '{field}'")
    name = meta.get("name", "")
    if name and name != skill_dir.name:
        errors.append(f"{skill_dir.name}: name '{name}' does not match directory name")
    if name and not re.match(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$", name):
        errors.append(f"{skill_dir.name}: invalid name format '{name}'")
    return errors


def validate_registry() -> Tuple[List[str], Dict[str, Any]]:
    errors: List[str] = []
    reg_path = ROOT / "references" / "awesome_agentic_stack.json"
    if not reg_path.exists():
        return ["Missing references/awesome_agentic_stack.json"], {}
    try:
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"Invalid JSON in registry: {e}"], {}
    repos = reg.get("repositories", [])
    if len(repos) != 50:
        errors.append(f"Registry has {len(repos)} repositories, expected 50")
    ids = [r.get("id") for r in repos]
    urls = [r.get("url") for r in repos]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate repository IDs found")
    if len(urls) != len(set(urls)):
        errors.append("Duplicate repository URLs found")
    for r in repos:
        ref = r.get("reference_file")
        if not ref:
            errors.append(f"Missing reference_file for {r.get('id')}")
            continue
        path = ROOT / "references" / ref
        if not path.exists():
            errors.append(f"Broken reference: {ref}")
    return errors, reg


def validate_schemas() -> List[str]:
    errors: List[str] = []
    schema_dir = ROOT / "skills" / "production-hardening" / "schemas"
    if schema_dir.exists():
        for p in schema_dir.glob("*.json"):
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                errors.append(f"Invalid schema {p.name}: {e}")
    return errors


def main() -> int:
    print("SKILL VALIDATION")
    print("=" * 50)
    skills_dir = ROOT / "skills"
    all_ok = True
    if skills_dir.exists():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                errs = validate_skill(d)
                status = "PASS" if not errs else "FAIL"
                if errs:
                    all_ok = False
                    for e in errs:
                        print(f"  ERROR: {e}")
                print(f"{d.name:<30} {status}")
    print()
    reg_errs, reg = validate_registry()
    print(f"{'Agentic Registry':<30} {'PASS' if not reg_errs else 'FAIL'}")
    if reg_errs:
        all_ok = False
        for e in reg_errs:
            print(f"  ERROR: {e}")
    count = len(reg.get("repositories", [])) if reg else 0
    print(f"{'Repository count':<30} {count}/50")
    if count != 50:
        all_ok = False
    broken = sum(1 for e in reg_errs if "Broken" in e)
    print(f"{'Broken references':<30} {broken}")
    print(f"{'Duplicate IDs':<30} {0 if not any('Duplicate repository IDs' in e for e in reg_errs) else 1}")
    schema_errs = validate_schemas()
    print(f"{'Invalid schemas':<30} {len(schema_errs)}")
    if schema_errs:
        all_ok = False
        for e in schema_errs:
            print(f"  ERROR: {e}")
    print()
    status = "PASSED" if all_ok else "FAILED"
    print(f"STATUS: {status}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
