---
name: context-optimizer
description: "Reduce context window and token usage for AI coding agents. Use when working with large repositories, large files, context overflow risks, or when the user asks to optimize tokens, compress prompts, or reduce context. Prefer targeted search (rg/grep) over full-file reads; ignore node_modules, .git, build artifacts, lockfiles and binaries."
---

## Trigger Criteria

Activate when:
- User mentions: reduce context, optimize tokens, compress prompt, large file edit, context overflow, huge repository, large codebase, reduce token usage
- Working in large monorepos or files > ~500 lines
- Approaching model context limits

## Core Rules

1. Do **not** read an entire large file when only a fragment is needed.
2. Prefer targeted search first: `rg`, `grep`, `find`, `git grep`.
3. Locate symbol / function / class first, then read a limited line range.
4. Never load without need:
   - `node_modules/`, `.git/`, `build/`, `dist/`, caches
   - lock files
   - binary files
5. For JSON: strip unnecessary whitespace while preserving structure and important fields.
6. Prefer compact structured output for large results.
7. Do not repeat already-known context.
8. Do not load the entire repository when the task is local.
9. Index / search first, then targeted read.
10. When a reference is needed from the agentic stack, load **one** file from `references/repositories/` after consulting the registry — never all 50.

## Expected Output

- Concise findings or edits
- Explicit file:line ranges used
- Token-conscious summaries instead of full dumps

## Limitations

- Does not replace model context limits; it reduces waste.
- Heuristic; agents must still respect host tool budgets.

## References

- `references/awesome_agentic_stack.json` (registry — filter, do not dump)
- `references/INDEX.md`
- `references/repositories/001-llmlingua.md` (context compression)
- `docs/AGENT_COMPATIBILITY.md`

## Examples

**Bad**: `cat src/huge_module.py`  
**Good**: `rg -n "def process_" src/` then read only the matching function range.

**Bad**: Load all 50 repository reference files.  
**Good**: Read registry → filter category `context-compression` → open only `001-llmlingua.md`.
