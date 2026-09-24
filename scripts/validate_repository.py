#!/usr/bin/env python3
"""Thin wrapper: same acceptance gate as `python -m agent_skills.cli validate`."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_skills.validate import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
