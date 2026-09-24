# Changelog

## v1.4.0 (finalization)

### Fixed / finalized

- Synchronized `awesome_agentic_stack.md` and `INDEX.md` with JSON registry (single source of truth)
- Full repository acceptance validator (`REPOSITORY ACCEPTED` only when all checks pass)
- JSON ↔ Markdown sync tests and negative validator test
- CI runs the same acceptance validator
- `docs/AI_AGENT_VERIFICATION.md` for AI agents

## v1.4.0

### Added

- Agent Skills validation CLI (`agent-skills validate`)
- Exactly 50 local repository reference files under `references/repositories/`
- Machine-readable registry `references/awesome_agentic_stack.json` (version 1.4.0)
- Repository index `references/INDEX.md`
- Project-local manifest `agent-skills.json`
- Agent compatibility documentation (`docs/AGENT_COMPATIBILITY.md`)
- Installation guide (`docs/INSTALLATION.md`)
- Architecture documentation (`docs/ARCHITECTURE.md`)
- Rules documentation (`docs/RULES.md`)
- Contributing guide (`docs/CONTRIBUTING.md`)
- Registry and skill validation tests
- `pyproject.toml` package metadata (version 1.4.0)

### Improved

- Production-hardening skill remains the primary security/reliability gate
- Context-optimizer skill documentation and triggers
- CI workflow includes skill and registry validation steps

### Tests

- Registry validation (exactly 50, unique IDs/URLs, all files present)
- Skill frontmatter validation
- Validator exit-code tests
- Existing hardening audit tests preserved

## v1.3.0

- Context-optimizer skill
- Awesome agentic stack markdown catalog
- CI fixes
