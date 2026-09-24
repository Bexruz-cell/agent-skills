# AI Agent Verification

This repository is a portable **Agent Skills** library with a machine-verifiable acceptance gate.

## How an AI agent should verify this repository

1. Locate the repository root.
2. Read `agent-skills.json` (project-local manifest).
3. Discover skills under `skills/*/SKILL.md`.
4. Discover the registry at `references/awesome_agentic_stack.json`.
5. Run the repository validator:

```bash
python -m agent_skills.cli validate --skip-heavy
# or
python scripts/validate_repository.py
# or
python agent_skills/validate.py --skip-heavy
```

6. For machine parsing:

```bash
python -m agent_skills.cli validate --json --skip-heavy
```

7. Accept the repository only if:

```json
{
  "accepted": true,
  "status": "accepted"
}
```

8. On success the human output ends with:

```text
REPOSITORY ACCEPTED
```

## Important

- `REPOSITORY ACCEPTED` is emitted by the validator only after all mandatory checks pass.
- It is not a static claim in documentation.
- Agents must run the validator; they must not assume acceptance without checking `accepted == true`.

## Selective reference loading

Do **not** load all 50 reference files into context.

1. Read `references/awesome_agentic_stack.json` or `references/INDEX.md`.
2. Filter by category.
3. Open a single `references/repositories/NNN-id.md` when needed.
