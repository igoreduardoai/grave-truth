#!/usr/bin/env python3
"""PreToolUse hook: exit 2 when a tool call targets a secret-looking path."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grave_truth.secret_guard import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
