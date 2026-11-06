#!/usr/bin/env python3
"""Offline lease checker. Quotes the synthetic residential lease."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grave_truth.cli import main  # noqa: E402


if __name__ == "__main__":
    question = sys.argv[1:] or ["What is the monthly rent?"]
    sys.exit(main(["lease", *question]))
