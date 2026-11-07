#!/usr/bin/env python3
"""Judge-readable transcript for both demo apps.

Prints question, answer, quote span, and pass/fail for every gold case.
Exits 0 only when every case passes. Synthetic fixtures. No network.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grave_truth.apps import eob, lease  # noqa: E402
from grave_truth.grading import evaluate_case  # noqa: E402

CASES = json.loads((ROOT / "evals" / "gold_cases.json").read_text(encoding="utf-8"))

APP_LABELS = {
    "eob": "eob-explainer",
    "lease": "lease-checker",
}


def _agent(app: str):
    if app == "eob":
        return eob.load_agent()
    if app == "lease":
        return lease.load_agent()
    raise ValueError(f"unknown app {app}")


def _transcript(case: dict, agent) -> tuple[bool, list[str]]:
    ok, detail = evaluate_case(case, agent)
    expect = case["expect"]
    if expect in {"reject_ungrounded", "accept_grounded"}:
        rejected = agent.reject_ungrounded_claim(case["question"])
        answer = "rejected" if rejected else "accepted"
        quote = "none"
    else:
        result = agent.answer(case["question"])
        answer = result.text
        quote = " || ".join(citation.span for citation in result.citations) or "none"
    status = "PASS" if ok else "FAIL"
    lines = [
        f"Case: {case['id']}",
        f"Question: {case['question']}",
        f"Answer: {answer}",
        f"Quote: {quote}",
        f"Result: {status}",
    ]
    if not ok:
        lines.append(f"Detail: {detail}")
    return ok, lines


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    counts: Counter[str] = Counter()
    failed = 0
    print("Grave Truth walkthrough")
    print("Synthetic fixtures only. Research demo: not a medical device and not legal advice.")
    print("Each block is question, answer, quote span, pass/fail.")
    for app in ("eob", "lease"):
        print()
        print(f"# {APP_LABELS[app]}")
        agent = _agent(app)
        for case in CASES:
            if case["app"] != app:
                continue
            counts[case["expect"]] += 1
            ok, lines = _transcript(case, agent)
            if not ok:
                failed += 1
            print()
            print("\n".join(lines))
    passed = len(CASES) - failed
    print()
    print(f"passed {passed}/{len(CASES)}")
    summary = ", ".join(f"{name} {counts[name]}" for name in sorted(counts))
    print(summary)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
