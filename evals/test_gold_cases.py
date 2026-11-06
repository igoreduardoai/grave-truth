import json
from pathlib import Path

from grave_truth.apps import eob, lease

CASES = json.loads((Path(__file__).parent / "gold_cases.json").read_text(encoding="utf-8"))


def _agent(app: str):
    return eob.load_agent() if app == "eob" else lease.load_agent()


def test_gold_cases_all_pass():
    assert len(CASES) >= 10
    for case in CASES:
        agent = _agent(case["app"])
        if case["expect"] == "reject_ungrounded":
            assert agent.reject_ungrounded_claim(case["question"]) is True, case["id"]
            continue
        result = agent.answer(case["question"])
        if case["expect"] == "not_found":
            assert result.found is False, case["id"]
            assert result.text == "not found", case["id"]
            continue
        assert result.found, case["id"]
        assert result.citations, case["id"]
        for needle in case.get("must_include", []):
            assert needle in result.text or any(needle in c.span for c in result.citations), case["id"]
