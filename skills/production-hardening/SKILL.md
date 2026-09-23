---
name: production-hardening
description: "Production hardening and reliability audit for Python/Node.js applications. Trigger before git commit, before deploy, when user asks for security audit, API resilience check, database pool review, performance optimization, race condition scan, secret leak detection, or production readiness review. Use when preparing code for production or investigating stability issues."
compatibility: claude-code, antigravity, gemini-cli, cursor, windsurf
version: 1.1.0
---

## Trigger Criteria

Activate this skill when:
- User is about to commit or push code to main/master
- User requests a security / production readiness audit
- User mentions: "harden", "production check", "security audit", "pool leak", "race condition", "secret scan", "before deploy", "API resilience"
- Code contains async workers, database connections, background tasks, or external API calls
- User asks to review stability, timeouts, or resource cleanup

## Execution Protocol

1. Load configuration from `schemas/audit_config.json`.
2. Run secret and high-entropy string scan across the repository (exclude paths listed in config).
3. Perform AST-based syntax and structural checks on Python files (HTTP-client context only).
4. Scan for common anti-patterns listed in `references/security_rules.md`:
   - Unclosed connection pools
   - Missing timeouts on HTTP clients
   - Unprotected shared state in async code
   - SQLite "database is locked" patterns
   - Hardcoded credentials
5. Execute `scripts/hardening_audit.py` with appropriate flags.
6. Collect findings and classify severity (CRITICAL / HIGH / MEDIUM / LOW).
7. Produce the standardized report defined in Output Format.
8. If CRITICAL findings exist, exit with non-zero status and block further automated actions until resolved.

## Token & Shell Safety

- Never cat entire large log files or directories. Always pipe through `head -n 50` or `Select-Object -First 50`.
- Prefer `rg` / `grep -n` with context limits over full-file reads.
- Limit AST walk depth and file size (skip files > 1 MB unless explicitly requested).
- When running the audit script, capture only structured JSON output.

## Security Boundaries

- Never print or log actual secret values — only report file:line and redacted fingerprint.
- Never modify source files automatically unless user explicitly requests a fix.
- Do not exfiltrate repository contents outside the local workspace.
- Respect `.gitignore` and the ignore list in `audit_config.json`.
- Test directories (`tests/`, `test_*.py`) are skipped by default.

## Verification Gate

Before declaring the audit complete:
- Confirm `hardening_audit.py` exited cleanly or with expected non-zero code.
- Confirm JSON report is valid.
- Confirm no raw secrets appear in the final output.
- Run basic syntax check (`python -m py_compile` on changed Python files) if fixes were proposed.

## Output Format

Always emit the report in this exact structure:

```
# Production Hardening Report

Status: PASSED | FAILED

## Summary
- Critical: N
- High: N
- Medium: N
- Low: N

## Findings
### [CRITICAL] <title>
- File: path:line
- Rule: <CWE / internal id>
- Description: ...
- Recommendation: ...

## Affected Files
- path/to/file1
- path/to/file2

## Next Actions
- <concrete steps>
```

If Status is FAILED, list the blocking issues first.

## Failure Modes & Known Limitations

- **Entropy analysis** can produce false positives on legitimate high-entropy strings (UUIDs, base64 blobs, minified identifiers). Always verify HIGH findings manually.
- **Minified / bundled JavaScript** is skipped by size limit and ignore patterns; run a dedicated JS secret scanner if needed.
- **Dynamic attribute access** (`getattr(obj, "get")`) is not detected by the AST checker.
- **HTTP client detection** relies on naming conventions (`requests`, `session`, `client`, `httpx`, …). Custom wrappers may be missed.
- The scanner does not execute code; it is purely static.

## Invocation Examples by Environment

### Claude Code / Antigravity CLI
```
/skill production-hardening
# or just mention: "run production hardening audit before commit"
```

### Cursor (Rules / Composer)
Add to `.cursor/rules` or ask:
```
Use the production-hardening skill and run a full audit on the current workspace.
```

### Gemini CLI
```
@production-hardening audit this repository before deploy
```

### Direct CLI
```bash
python skills/production-hardening/scripts/hardening_audit.py --root . --json
```
