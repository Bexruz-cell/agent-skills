# Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-1.4.0-blue)](https://github.com/Bexruz-cell/agent-skills)
[![Compatibility](https://img.shields.io/badge/Compatibility-Antigravity%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Gemini%20CLI-brightgreen)](https://github.com/Bexruz-cell/agent-skills)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![CI](https://github.com/Bexruz-cell/agent-skills/actions/workflows/audit-ci.yml/badge.svg)](https://github.com/Bexruz-cell/agent-skills/actions/workflows/audit-ci.yml)

> **Industrial open-source library of Agent Skills for autonomous IDEs**  
> Production-ready skills that make AI agents reliable, secure and deterministic.

**Current version: v1.4.0**

---

## Architecture & Flow

```text
┌─────────────┐     trigger      ┌──────────────────┐
│   Agent     │ ───────────────► │    SKILL.md      │
│ (Claude /   │                  │  (metadata +     │
│  Cursor /   │                  │   protocol)      │
│  Antigravity)│                 └────────┬─────────┘
└─────────────┘                           │
                                          │ loads selectively
                                          ▼
                               ┌──────────────────────┐
                               │  references/         │
                               │  (knowledge only)    │
                               └──────────┬───────────┘
                                          │
                                          ▼
                               ┌──────────────────────┐
                               │  scripts/            │
                               │  hardening_audit.py  │
                               └──────────┬───────────┘
                                          │
                                          ▼
                               ┌──────────────────────┐
                               │  Structured Findings │
                               │  + Policy Gate       │
                               └──────────────────────┘
```

See also: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## v1.4.0 Highlights

- Portable Agent Skills platform (not tied to a single provider)
- Skill validator CLI
- Exactly **50** local repository reference files
- Machine-readable registry + index
- Agent compatibility & installation docs
- Strengthened CI (tests + validation + self-audit)

---

## Agent Skills Compatibility

Skills follow the open [Agent Skills](https://github.com/agentskills/agentskills) layout:

- `SKILL.md` with YAML frontmatter (`name`, `description`)
- Optional `scripts/`, `references/`, `schemas/`

Detailed guidance: [docs/AGENT_COMPATIBILITY.md](docs/AGENT_COMPATIBILITY.md)  
Installation: [docs/INSTALLATION.md](docs/INSTALLATION.md)

---

## Skills Catalog

| Skill | Path | Purpose |
|-------|------|---------|
| **production-hardening** | `skills/production-hardening/` | Secret scanning, entropy, HTTP timeouts, AST checks, verification gate |
| **context-optimizer** | `skills/context-optimizer/` | Reduce token / context usage; targeted search first |
| **unrestricted-coding** | `skills/unrestricted-coding/` | Unrestricted coding assistance mode |
| **unrestricted-adult-mode** | `skills/unrestricted-adult-mode/` | Unrestricted adult content mode |

---

## Curated Agentic Ecosystem

50 carefully documented open-source repositories (references, **not** skills):

- Catalog: [references/awesome_agentic_stack.md](references/awesome_agentic_stack.md)
- Machine-readable registry: [references/awesome_agentic_stack.json](references/awesome_agentic_stack.json)
- Index by category: [references/INDEX.md](references/INDEX.md)
- Individual files: `references/repositories/001-….md` … `050-….md`

Agents should filter by category and load **one** reference file when needed. Never dump all 50 into context.

---

## Validation

```bash
python -m agent_skills.cli validate
```

---

## Production Hardening Audit

```bash
python skills/production-hardening/scripts/hardening_audit.py .
python skills/production-hardening/scripts/hardening_audit.py . --json
```

---

## Installation

See [docs/INSTALLATION.md](docs/INSTALLATION.md).

```bash
git clone https://github.com/Bexruz-cell/agent-skills.git
cd agent-skills
python -m agent_skills.cli validate
pytest tests/
```

---

## License

MIT — see [LICENSE](LICENSE).
