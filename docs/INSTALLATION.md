# Installation

## Clone

```bash
git clone https://github.com/Bexruz-cell/agent-skills.git
cd agent-skills
```

## Use with a compatible agent

Point the agent at the `skills/` directory (exact mechanism depends on the host):

- **Claude Code / Antigravity-style**: register the skills path.
- **Cursor**: add skills folder or rules that reference `SKILL.md`.
- **Generic**: instruct the agent to load `skills/*/SKILL.md` on relevant triggers.

## Validate locally

```bash
python -m agent_skills.cli validate
# or
python agent_skills/validate.py
```

## Run production hardening audit

```bash
python skills/production-hardening/scripts/hardening_audit.py .
python skills/production-hardening/scripts/hardening_audit.py . --json
```

## Run tests

```bash
pip install pytest
pytest tests/
```

## Python package (optional)

```bash
pip install -e .
agent-skills validate
```
