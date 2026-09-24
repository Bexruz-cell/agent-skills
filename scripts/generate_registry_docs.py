#!/usr/bin/env python3
"""Generate awesome_agentic_stack.md and INDEX.md from the JSON registry (source of truth)."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    reg = json.loads((ROOT / "references" / "awesome_agentic_stack.json").read_text(encoding="utf-8"))
    repos = reg["repositories"]
    if len(repos) != 50:
        raise SystemExit(f"Expected 50 repositories, got {len(repos)}")

    lines = [
        "# Awesome Agentic Stack\n\n",
        "> Curated reference knowledge base of 50 open-source repositories useful for AI coding agents.\n\n",
        f"**Version**: {reg['version']}  \n",
        "**Machine-readable registry**: [`awesome_agentic_stack.json`](awesome_agentic_stack.json)  \n",
        "**Index**: [`INDEX.md`](INDEX.md)\n\n",
        "These are **reference files**, not Agent Skills. Skills live under `skills/`.\n",
        "Agents should discover the registry, filter by category, and load only the specific reference files they need.\n\n",
        "---\n\n",
    ]
    for i, r in enumerate(repos, 1):
        lines.append(f"## {i:02d} — {r['name']}\n\n")
        lines.append(f"**Repository**: `{r['repository']}`  \n")
        lines.append(f"**URL**: {r['url']}  \n")
        lines.append(f"**Category**: {r['category']}  \n")
        lines.append(f"**Purpose**: {r.get('purpose', '')}  \n")
        lines.append(f"**Agent relevance**: {r.get('agent_relevance', '')}  \n")
        lines.append(f"**License**: {r.get('license', '')}  \n")
        lines.append(f"**Reference**: [`{r['reference_file']}`]({r['reference_file']})\n\n")
        lines.append("---\n\n")
    (ROOT / "references" / "awesome_agentic_stack.md").write_text("".join(lines), encoding="utf-8")

    cats: dict = defaultdict(list)
    for r in repos:
        cats[r["category"]].append(r)
    idx = [
        "# Repository Index\n\n",
        "Machine-readable registry: `references/awesome_agentic_stack.json`\n\n",
        "Total repositories: **50**\n\n",
        "## By Category\n",
    ]
    for cat in sorted(cats):
        idx.append(f"\n### {cat}\n\n")
        for r in cats[cat]:
            idx.append(f"- `{r['id']}` — [{r['name']}]({r['reference_file']}) ({r['repository']})\n")
    idx.append("\n## All Repositories (numeric)\n\n")
    idx.append("| # | ID | Name | Category | Repository |\n|---|----|------|----------|------------|\n")
    for r in repos:
        num = r["reference_file"].split("/")[-1][:3]
        idx.append(f"| {num} | `{r['id']}` | {r['name']} | {r['category']} | [{r['repository']}]({r['url']}) |\n")
    (ROOT / "references" / "INDEX.md").write_text("".join(idx), encoding="utf-8")
    print(f"Generated docs for {len(repos)} repositories from JSON source of truth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
