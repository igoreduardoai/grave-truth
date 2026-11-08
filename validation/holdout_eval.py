"""Held-out adversarial cases. The snapshot is the first measurement, not a tuned target."""

from __future__ import annotations

import json
from pathlib import Path

from grave_truth.grading import evaluate_case
from grave_truth.skeleton import DocumentAgent

ROOT = Path(__file__).resolve().parents[1]


def measure(root: Path | None = None) -> dict:
    root = root or ROOT
    cases = json.loads((root / "evals" / "holdout_cases.json").read_text(encoding="utf-8"))
    rows = []
    met = 0
    for case in cases:
        agent = DocumentAgent()
        agent.ingest(case.get("doc_id", "pasted-document"), case["document"])
        result = agent.answer(case["question"])
        ok, detail = evaluate_case(case, agent)
        met += int(ok)
        rows.append({
            "id": case["id"],
            "group": case.get("group"),
            "intended": case["expect"],
            "intended_met": bool(ok),
            "detail": detail,
            "conflict": result.conflict,
            "found": result.found,
            "text": result.text,
            "spans": [citation.span for citation in result.citations],
            "note": case.get("note", ""),
        })
    return {"intended_met": met, "attempted": len(cases), "cases": rows}


def load_snapshot(root: Path | None = None) -> dict:
    root = root or ROOT
    return json.loads((root / "evals" / "holdout_observed.json").read_text(encoding="utf-8"))
