#!/usr/bin/env python3
"""Eval runner intended to be invoked by the Kiro hook on save."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from grave_truth.apps import eob, lease
from grave_truth.grading import evaluate_case

ROOT = Path(__file__).resolve().parent
CASES = json.loads((ROOT / "gold_cases.json").read_text(encoding="utf-8"))


def _agent(app: str):
    if app == "eob":
        return eob.load_agent()
    if app == "lease":
        return lease.load_agent()
    raise ValueError(f"unknown app {app}")


def main() -> int:
    failed = 0
    counts: Counter[str] = Counter()
    for case in CASES:
        counts[case["expect"]] += 1
        ok, detail = evaluate_case(case, _agent(case["app"]))
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
            print(f"{status}  {case['id']}  {detail}")
        else:
            print(f"{status}  {case['id']}")
    passed = len(CASES) - failed
    print(f"{passed}/{len(CASES)} passed")
    summary = ", ".join(f"{name} {counts[name]}" for name in sorted(counts))
    print(summary)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
