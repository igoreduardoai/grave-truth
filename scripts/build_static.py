#!/usr/bin/env python3
"""Write site/ for a later static host. Does not deploy and does not call a model."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grave_truth.static_site import build  # noqa: E402


def main() -> int:
    dest = ROOT / "site"
    build(dest)
    print(f"Wrote {dest}")
    print("Not deployed. The live check is still python3 demos/haunted/server.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
