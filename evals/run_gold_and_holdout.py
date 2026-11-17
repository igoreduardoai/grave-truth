#!/usr/bin/env python3
"""Run the gold suite, then compare the held-out snapshot. Does not edit either file."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    gold = subprocess.run([sys.executable, str(ROOT / "evals" / "run_evals.py")], cwd=ROOT)
    if gold.returncode != 0:
        return gold.returncode
    sys.path.insert(0, str(ROOT / "src"))
    sys.path.insert(0, str(ROOT))
    from validation.holdout_eval import load_snapshot, measure

    current = measure(ROOT)
    snapshot = load_snapshot(ROOT)
    observed = [(row["id"], row["intended_met"], row["text"]) for row in current["cases"]]
    recorded = [(row["id"], row["intended_met"], row["text"]) for row in snapshot["cases"]]
    print(f"holdout {current['intended_met']}/{current['attempted']}")
    if observed != recorded or current["intended_met"] != current["attempted"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
