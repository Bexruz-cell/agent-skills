---
name: context-optimizer
version: 1.0.0
type: token-efficiency
description: "Context optimization and token efficiency protocol for AI agents. Enforces targeted search (rg/grep) instead of full-file reading, ignores lockfiles, minified bundles and binaries, truncates large outputs, and formats dense responses in structured JSON to prevent context window overflow."
compatibility: claude-code, antigravity, gemini-cli, cursor, windsurf
---

## Trigger Criteria

Activate this skill when:
- User mentions: "reduce context", "optimize tokens", "compress prompt", "large file edit", "context overflow"
- Working in large repositories with deep directory structures or high token consumption
- Reading or refactoring files exceeding 500 lines or 50 KB
- Inspecting test logs, build traces, or dependency graphs
- Approaching model context window limits or managing strict token budgets

## Execution Protocol

1. **Targeted Code Retrieval (Ripgrep / Grep First)**:
   - Never read full files when searching for definitions, usages, or patterns.
   - Use `rg -n -C 2 "<pattern>"` or targeted search tools to locate exact lines.
   - Read only specific line ranges (e.g. `view_file` with `StartLine` and `EndLine`) containing relevant blocks.

2. **Strict File Filtering & Exclusions**:
   - Completely ignore dependency lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`, `Pipfile.lock`, `Cargo.lock`, `composer.lock`).
   - Skip generated build artifacts (`dist/`, `build/`, `out/`, `coverage/`, `.next/`).
   - Skip minified code (`*.min.js`, `*.bundle.js`, `*.min.css`) and sourcemaps (`*.map`).
   - Never open binary files, compiled assets (`*.pyc`, `*.wasm`, `*.so`, `*.dll`), or sqlite databases directly.

3. **Shell & Output Limiting (Select-Object / Head)**:
   - Cap command outputs using `head -n 50`, `tail -n 50`, or PowerShell `Select-Object -First 50`.
   - Never run raw `cat` or print full directory dumps without filtering.
   - Redirect verbose compilation or test outputs to temporary logs and grep for failures only.

4. **Prompt & Context Compression**:
   - Eliminate conversational filler, redundant greetings, and speculative explanations.
   - Extract and state only essential facts, file paths, diffs, and validation results.
   - Keep tool call inputs tight and avoid passing repetitive prompt instructions.

5. **Structured JSON Output**:
   - For multi-item results, audits, or status summaries, format output as dense, machine-readable JSON without extraneous prose.

## Security & Reliability Boundaries

- Do not bypass verification gates when optimizing context — critical checks and tests must always run.
- Do not compress out critical error messages, stack traces, or validation failures.
- Always preserve line numbers and exact filenames when reporting findings.

## Output Format

When summarizing optimization actions or structured findings:

```json
{
  "status": "OPTIMIZED",
  "files_filtered": [
    "package-lock.json",
    "dist/*"
  ],
  "retrieval_method": "targeted_grep",
  "token_savings_estimate": "high",
  "summary": "Context pruned: lockfiles ignored, targeted AST/grep retrieval applied."
}
```
