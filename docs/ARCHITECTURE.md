# Architecture

```
Agent
  ↓ discovers
Skill (SKILL.md)
  ↓ loads selectively
References (knowledge)
  ↓ invokes
Scripts (deterministic tools)
  ↓ uses
Detectors / Rules
  ↓ emits
Structured Findings (JSON)
  ↓ evaluated by
Policy (PASS / WARN / FAIL)
  ↓ enforces
Verification Gate
```

## Design principle

**Agent Skills = Instructions + Deterministic Tools + References + Schemas + Validation + CI + Machine-readable Registry**

- `SKILL.md` → agent behaviour and triggers
- `scripts/` → deterministic, testable actions
- `schemas/` → machine contracts
- `references/` → knowledge base (not skills)
- `rules/` → detection logic
- `tests/` → verification
- `CI` → automatic checks
- `registry` → discovery

## 50 repositories are reference knowledge

They live under `references/repositories/` and are catalogued by:

- `references/awesome_agentic_stack.md`
- `references/awesome_agentic_stack.json`
- `references/INDEX.md`

They are **not** individual skills.
A skill (e.g. `context-optimizer`) may *point* at a reference such as `001-llmlingua.md`, but LLMLingua itself is not a skill.
