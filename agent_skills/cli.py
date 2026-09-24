#!/usr/bin/env python3
"""CLI entry point for agent-skills."""
from __future__ import annotations
import sys

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: agent-skills <command> [options]")
        print("Commands: validate [--json] [--skip-heavy]")
        return 1
    cmd = sys.argv[1]
    if cmd == "validate":
        from agent_skills.validate import main as validate_main
        return validate_main(sys.argv[2:])
    print(f"Unknown command: {cmd}")
    return 1

if __name__ == "__main__":
    sys.exit(main())
