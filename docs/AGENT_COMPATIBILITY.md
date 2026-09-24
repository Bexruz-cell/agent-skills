# Agent Compatibility

This repository follows the [Agent Skills](https://github.com/agentskills/agentskills) open format.

## Standard skill layout

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + instructions
├── scripts/          # Optional: deterministic tools
├── references/       # Optional: supporting docs
├── schemas/          # Optional: machine contracts
└── tests/            # Optional
```

## How an AI agent should consume this repository

1. **Discover** `skills/` — list directories that contain `SKILL.md`.
2. **Read** only the frontmatter (name + description) of each skill for matching.
3. **Match** description / triggers to the current user task.
4. **Load** the full `SKILL.md` only for the matched skill(s).
5. **Load only relevant references** — never dump all 50 repository files into context.
   - Start from `references/awesome_agentic_stack.json` or `references/INDEX.md`.
   - Filter by category.
   - Open a single `references/repositories/NNN-id.md` when needed.
6. **Execute** deterministic scripts under `scripts/` when the skill protocol requires it.
7. **Consume** structured JSON output (findings, reports).
8. **Apply** policy / verification gate (PASS / WARN / FAIL).
9. **Return** a structured result to the user or downstream agent.

## Universal parts

- `SKILL.md` with `name` and `description` frontmatter
- Directory-per-skill layout
- Optional `scripts/`, `references/`, `schemas/`

## Adapters may be needed for

| Agent            | Notes                                      |
|------------------|--------------------------------------------|
| Claude Code      | Native skill discovery                     |
| Cursor           | Rules / skills folders                     |
| Gemini CLI       | May need explicit skill path               |
| Codex-style      | Prompt + tool injection                    |
| VS Code agents   | Extension-specific loading                 |

This is **not** a claim that every agent supports the format identically.
Adapters or thin wrappers may be required for non-standard hosts.

## Project-local manifest

See `agent-skills.json` (project-local, not an official standard).
