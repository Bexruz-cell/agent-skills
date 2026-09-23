# Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-1.0-blue)](https://github.com/Bexruz-cell/agent-skills)
[![Compatibility](https://img.shields.io/badge/Compatibility-Antigravity%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Gemini%20CLI-brightgreen)](https://github.com/Bexruz-cell/agent-skills)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)

> **Industrial open-source library of Agent Skills for autonomous IDEs**  
> Production-ready skills that make AI agents reliable, secure and deterministic.

---

## Architecture & Flow

```text
┌─────────────┐     trigger      ┌──────────────────┐
│   Agent     │ ───────────────► │    SKILL.md      │
│ (Claude /   │                  │  (metadata +     │
│  Cursor /   │                  │   protocol)      │
│  Antigravity)│                 └────────┬─────────┘
└─────────────┘                           │
                                          │ loads
                                          ▼
                               ┌──────────────────────┐
                               │  references/         │
                               │  security_rules.md   │
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
                               │  Structured Report   │
                               │  (PASSED / FAILED)   │
                               │  + JSON output       │
                               └──────────────────────┘
```

**Mermaid version:**

```mermaid
flowchart LR
    A[Agent] -->|Trigger keywords| B[SKILL.md]
    B --> C[Load security_rules.md]
    B --> D[Run hardening_audit.py]
    D --> E[JSON Report]
    E --> F{Gate}
    F -->|PASSED| G[Continue]
    F -->|FAILED| H[Block / Fix]
```

---

## Skills Catalog

| Skill | Purpose | Environments | Trigger |
|-------|---------|--------------|---------|
| **production-hardening** | Security audit, secret scan, race-condition & pool leak detection, production readiness | Antigravity, Claude Code, Cursor, Gemini CLI, Windsurf | `before commit`, `security audit`, `harden`, `before deploy`, `pool leak`, `race condition` |

---

## Quickstart

### 1. Clone or copy the skill

```bash
git clone https://github.com/Bexruz-cell/agent-skills.git
```

Copy the skill into your agent skills directory:

```bash
# Claude Code / Antigravity style
cp -r agent-skills/skills/production-hardening ~/.claude/skills/
# or
cp -r agent-skills/skills/production-hardening .agent/skills/
```

### 2. Run the audit CLI directly

```bash
cd agent-skills/skills/production-hardening
python scripts/hardening_audit.py --root /path/to/your/project --json
```

### 3. Example JSON report

```json
{
  "status": "FAILED",
  "summary": {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 0,
    "files_scanned": 47
  },
  "findings": [
    {
      "severity": "CRITICAL",
      "rule": "hardcoded-secret-regex",
      "file": "src/config.py",
      "line": 14,
      "fingerprint": "AKIAI…XAMPLE",
      "description": "Matched secret pattern: AKIA[0-9A-Z]{16}",
      "recommendation": "Move secret to environment variable or secret manager and rotate it."
    }
  ]
}
```

---

## Project Structure

```text
agent-skills/
├── README.md
├── LICENSE
└── skills/
    └── production-hardening/
        ├── SKILL.md
        ├── references/
        │   └── security_rules.md
        ├── schemas/
        │   └── audit_config.json
        └── scripts/
            └── hardening_audit.py
```

---

## License

MIT © 2026 Bexruz-cell
