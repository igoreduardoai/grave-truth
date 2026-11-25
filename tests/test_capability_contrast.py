"""Measured with/without counts. The numbers in the matrix have to match these."""

import json
from pathlib import Path

from grave_truth.apps import eob, lease
from grave_truth.artifact import build_artifact

ROOT = Path(__file__).resolve().parents[1]


def _not_found_cases() -> list[dict]:
    cases = json.loads((ROOT / "evals" / "gold_cases.json").read_text(encoding="utf-8"))
    return [case for case in cases if case["expect"] == "not_found"]


def test_cite_or_abstain_cites_zero_of_the_not_found_cases():
    """A first-sentence quoter cites every abstention. The checker cites none."""
    false_agent = 0
    false_naive = 0
    for case in _not_found_cases():
        agent = eob.load_agent() if case["app"] == "eob" else lease.load_agent()
        result = agent.answer(case["question"])
        if result.citations:
            false_agent += 1
        fixture = eob.FIXTURE if case["app"] == "eob" else lease.FIXTURE
        first = fixture.read_text(encoding="utf-8").splitlines()[0]
        if first:
            false_naive += 1
    assert false_agent == 0
    assert false_naive == 17
    assert len(_not_found_cases()) == 17


def test_export_attaches_two_spans_per_app_and_a_copy_attaches_none():
    linked = 0
    for app in ("eob", "lease"):
        artifact = build_artifact(app)
        linked += sum(len(item["citations"]) for item in artifact["items"])
    naive_linked = 0
    assert linked == 4
    assert naive_linked == 0
