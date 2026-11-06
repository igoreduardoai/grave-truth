#!/usr/bin/env python3
"""Eval runner intended to be invoked by the Kiro hook on save."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from grave_truth.apps import eob, lease

ROOT = Path(__file__).resolve().parent
CASES = json.loads((ROOT / "gold_cases.json").read_text(encoding="utf-8"))


def _agent(app: str):
    return eob.load_agent() if app == "eob" else lease.load_agent()


def main() -> int:
    failed = 0
    for case in CASES:
        agent = _agent(case["app"])
        if case["expect"] == "reject_ungrounded":
            ok = agent.reject_ungrounded_claim(case["question"]) is True
        else:
            result = agent.answer(case["question"])
            if case["expect"] == "not_found":
                ok = result.found is False and result.text == "not found"
            else:
                ok = result.found and bool(result.citations)
                for needle in case.get("must_include", []):
                    ok = ok and (needle in result.text or any(needle in c.span for c in result.citations))
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"{status}  {case['id']}")
    print(f"{len(CASES) - failed}/{len(CASES)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
