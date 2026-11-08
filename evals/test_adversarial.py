"""Development adversarial cases. These were used while checking the conflict rule.

Held-out cases live in holdout_cases.json and are not part of this file.
"""

import json
from pathlib import Path

from grave_truth.grading import evaluate_case
from grave_truth.skeleton import DocumentAgent

CASES = json.loads((Path(__file__).parent / "adversarial_cases.json").read_text(encoding="utf-8"))


def _agent(case: dict) -> DocumentAgent:
    agent = DocumentAgent()
    agent.ingest(case.get("doc_id", "pasted-document"), case["document"])
    return agent


def test_adversarial_cases_match_the_conflict_rule():
    assert len(CASES) == 8
    for case in CASES:
        ok, detail = evaluate_case(case, _agent(case))
        assert ok, f"{case['id']}: {detail}"


def test_conflict_answer_is_stable():
    case = CASES[0]
    agent = _agent(case)
    first = agent.answer(case["question"])
    second = agent.answer(case["question"])
    assert first.conflict and second.conflict
    assert [item.span for item in first.citations] == [item.span for item in second.citations]
    assert first.text == second.text
