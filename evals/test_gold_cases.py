import json
from collections import Counter
from pathlib import Path

from grave_truth.apps import eob, lease
from grave_truth.grading import evaluate_case

CASES = json.loads((Path(__file__).parent / "gold_cases.json").read_text(encoding="utf-8"))


def _agent(app: str):
    return eob.load_agent() if app == "eob" else lease.load_agent()


def test_gold_cases_all_pass():
    counts = Counter(case["expect"] for case in CASES)
    assert len(CASES) >= 24
    assert counts["cited"] >= 10
    assert counts["not_found"] >= 4
    assert counts["reject_ungrounded"] >= 4
    assert counts["accept_grounded"] >= 3
    for case in CASES:
        ok, detail = evaluate_case(case, _agent(case["app"]))
        assert ok, f"{case['id']}: {detail}"
