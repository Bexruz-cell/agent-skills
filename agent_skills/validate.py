#!/usr/bin/env python3
"""Repository-level acceptance validator for Bexruz Agent Skills."""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
VERSION = "1.4.0"

def parse_frontmatter(text: str) -> Dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    meta: Dict[str, Any] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta

def load_registry() -> Tuple[Optional[Dict], List[str]]:
    p = ROOT / "references" / "awesome_agentic_stack.json"
    if not p.exists():
        return None, ["missing registry JSON"]
    try:
        return json.loads(p.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as e:
        return None, [str(e)]

def run_all(include_heavy: bool = True) -> Dict[str, Any]:
    checks: Dict[str, Dict[str, str]] = {}
    def ok(name: str, detail: str = "") -> None:
        checks[name] = {"status": "pass", "detail": detail}
    def fail(name: str, detail: str) -> None:
        checks[name] = {"status": "fail", "detail": detail}

    need = ["skills", "references/repositories", "references/awesome_agentic_stack.json",
            "references/awesome_agentic_stack.md", "references/INDEX.md", "agent-skills.json",
            "README.md", ".github/workflows/audit-ci.yml"]
    miss = [x for x in need if not (ROOT / x).exists()]
    fail("structure", f"missing {miss}") if miss else ok("structure")

    skill_dirs = [d for d in (ROOT / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").exists()] if (ROOT / "skills").exists() else []
    serr: List[str] = []
    for d in skill_dirs:
        meta = parse_frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
        for f in ("name", "description"):
            if not meta.get(f):
                serr.append(f"{d.name}: missing {f}")
        if meta.get("name") and meta["name"] != d.name:
            serr.append(f"{d.name}: name mismatch")
    fail("skills", "; ".join(serr)) if serr or not skill_dirs else ok("skills", f"{len(skill_dirs)} skills")

    co = ROOT / "skills" / "context-optimizer" / "SKILL.md"
    if not co.exists():
        fail("context_optimizer", "missing")
    else:
        t = co.read_text(encoding="utf-8").lower()
        if not any(x in t for x in ("rg", "grep")) or "context" not in t:
            fail("context_optimizer", "missing guidance")
        else:
            ok("context_optimizer")

    ph = ROOT / "skills" / "production-hardening"
    if not (ph / "SKILL.md").exists() or not (ph / "scripts" / "hardening_audit.py").exists():
        fail("production_hardening", "missing files")
    else:
        ok("production_hardening")

    reg, rerr = load_registry()
    reg_details = {"count": 0, "unique_ids": 0, "unique_urls": 0, "files_on_disk": 0, "broken": 0}
    if rerr or reg is None:
        fail("registry", "; ".join(rerr))
    else:
        repos = reg.get("repositories", [])
        ids = [r.get("id") for r in repos]
        urls = [r.get("url") for r in repos]
        rnames = [r.get("repository") for r in repos]
        files = list((ROOT / "references" / "repositories").glob("*.md"))
        broken = sum(1 for r in repos if not r.get("reference_file") or not (ROOT / "references" / r["reference_file"]).exists())
        reg_details = {
            "count": len(repos), "unique_ids": len(set(ids)), "unique_urls": len(set(urls)),
            "files_on_disk": len(files), "broken": broken,
        }
        errs = []
        if len(repos) != 50: errs.append(f"count {len(repos)}")
        if len(ids) != len(set(ids)): errs.append("dup IDs")
        if len(urls) != len(set(urls)): errs.append("dup URLs")
        if len(rnames) != len(set(rnames)): errs.append("dup repos")
        if len(files) != 50: errs.append(f"disk {len(files)}")
        if broken: errs.append(f"broken {broken}")
        fail("registry", "; ".join(errs)) if errs else ok("registry")

    if reg:
        md_path = ROOT / "references" / "awesome_agentic_stack.md"
        md = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
        jrepos = {r["repository"] for r in reg["repositories"]}
        mrepos = set(re.findall(r"\*\*Repository\*\*: `([^`]+)`", md))
        jurls = {r["url"] for r in reg["repositories"]}
        murls = set(re.findall(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", md))
        if mrepos != jrepos or not jurls.issubset(murls):
            fail("json_markdown", f"mismatch j-only={sorted(jrepos-mrepos)[:3]} m-only={sorted(mrepos-jrepos)[:3]}")
        else:
            ok("json_markdown")
    else:
        fail("json_markdown", "no registry")

    if reg and (ROOT / "references" / "INDEX.md").exists():
        idx = (ROOT / "references" / "INDEX.md").read_text(encoding="utf-8")
        miss = [r["id"] for r in reg["repositories"] if f"`{r['id']}`" not in idx]
        fail("index", f"missing {miss[:5]}") if miss else ok("index")
    else:
        fail("index", "missing")

    verr = []
    for f in ("pyproject.toml", "agent-skills.json", "README.md"):
        if VERSION not in (ROOT / f).read_text(encoding="utf-8"):
            verr.append(f)
    if reg and reg.get("version") != VERSION:
        verr.append("registry")
    fail("version", str(verr)) if verr else ok("version", VERSION)

    wf = ROOT / ".github" / "workflows" / "audit-ci.yml"
    if not wf.exists() or "validate" not in wf.read_text(encoding="utf-8"):
        fail("ci", "missing validate step")
    else:
        ok("ci")

    dmiss = [p for p in ("docs/AGENT_COMPATIBILITY.md", "docs/INSTALLATION.md", "docs/ARCHITECTURE.md", "README.md", "CHANGELOG.md") if not (ROOT / p).exists()]
    fail("documentation", str(dmiss)) if dmiss else ok("documentation")

    pats = [re.compile(r"ghp_[A-Za-z0-9]{36}"), re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
            re.compile(r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----"), re.compile(r"AKIA[0-9A-Z]{16}")]
    skip = {".git", "__pycache__", "tests", "node_modules", "venv", ".venv"}
    skip_names = {"test_hardening_audit.py", "security_rules.md", "validate.py"}
    findings = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(s in path.parts for s in skip) or path.name in skip_names:
            continue
        if path.suffix in {".png", ".jpg", ".heic", ".pdf"} or path.stat().st_size > 500_000:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat in pats:
            if pat.search(text):
                findings.append(str(path.relative_to(ROOT)))
                break
    fail("security", "; ".join(findings[:5])) if findings else ok("security")

    if include_heavy:
        r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no"], cwd=str(ROOT), capture_output=True, text=True, timeout=120)
        fail("tests", (r.stdout + r.stderr)[-400:]) if r.returncode else ok("tests")
        script = ROOT / "skills" / "production-hardening" / "scripts" / "hardening_audit.py"
        r2 = subprocess.run([sys.executable, str(script), str(ROOT), "--json"], cwd=str(ROOT), capture_output=True, text=True, timeout=120)
        fail("production_audit", (r2.stdout or r2.stderr)[-400:]) if r2.returncode else ok("production_audit")

    all_ok = all(c["status"] == "pass" for c in checks.values())
    return {
        "repository": "Bexruz-cell/agent-skills",
        "version": VERSION,
        "status": "accepted" if all_ok else "rejected",
        "accepted": all_ok,
        "checks": checks,
        "skills": {"status": checks.get("skills", {}).get("status", "fail")},
        "registry": {
            "status": checks.get("registry", {}).get("status", "fail"),
            "repositories": reg_details["count"],
            "unique_ids": reg_details["unique_ids"],
            "unique_urls": reg_details["unique_urls"],
            "files_on_disk": reg_details["files_on_disk"],
            "broken": reg_details["broken"],
        },
        "references": {
            "status": "pass" if reg_details["broken"] == 0 and reg_details["count"] == 50 else "fail",
            "total": reg_details["count"],
            "broken": reg_details["broken"],
            "duplicates": 0 if reg_details["unique_ids"] == 50 else 1,
        },
        "tests": {"status": checks.get("tests", {}).get("status", "skipped")},
    }

def print_human(payload: Dict[str, Any]) -> None:
    print("=" * 50)
    print("BEXRUZ AGENT SKILLS")
    print("REPOSITORY VALIDATION")
    print("=" * 50)
    print(f"\nRepository:\n{payload['repository']}\n\nVersion:\n{payload['version']}\n")
    labels = [
        ("structure", "Structure"), ("skills", "Skills"), ("context_optimizer", "Context Optimizer"),
        ("production_hardening", "Production Hardening"), ("registry", "Reference Registry"),
        ("json_markdown", "JSON ↔ Markdown"), ("index", "INDEX"), ("version", "Version"),
        ("ci", "CI Configuration"), ("documentation", "Documentation"), ("security", "Security"),
        ("tests", "Tests"), ("production_audit", "Production Audit"),
    ]
    for key, label in labels:
        if key not in payload["checks"]:
            continue
        st = payload["checks"][key]["status"].upper()
        print(f"{label}:\n{st}")
        if payload["checks"][key].get("detail") and st != "PASS":
            print(f"  {payload['checks'][key]['detail']}")
        print()
    reg = payload["registry"]
    print(f"Repositories:\n{reg['repositories']} / 50\n")
    print(f"Unique repositories:\n{reg['unique_ids']} / 50\n")
    print(f"Unique IDs:\n{reg['unique_ids']} / 50\n")
    print(f"Unique URLs:\n{reg['unique_urls']} / 50\n")
    print(f"Reference files:\n{reg['files_on_disk']} / 50\n")
    print(f"Broken references:\n{reg['broken']}\n")
    print("=" * 50)
    print("FINAL STATUS")
    print("=" * 50)
    print()
    if payload["accepted"]:
        print("REPOSITORY ACCEPTED")
    else:
        print("REPOSITORY NOT ACCEPTED\n\nFailures:")
        for k, v in payload["checks"].items():
            if v["status"] != "pass":
                print(f"- {k}: {v.get('detail') or 'fail'}")
    print("=" * 50)

def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--skip-heavy", action="store_true")
    args = p.parse_args(argv)
    payload = run_all(include_heavy=not args.skip_heavy)
    if args.json:
        json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print_human(payload)
    return 0 if payload["accepted"] else 1

if __name__ == "__main__":
    sys.exit(main())
