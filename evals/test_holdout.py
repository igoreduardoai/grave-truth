"""The held-out file is compared with the first measurement. It is not a accuracy claim."""

import json
from pathlib import Path

from validation.holdout_eval import load_snapshot, measure

ROOT = Path(__file__).resolve().parents[1]


def test_holdout_measurement_matches_the_recorded_snapshot():
    current = measure(ROOT)
    snapshot = load_snapshot(ROOT)
    assert current["attempted"] == snapshot["attempted"] == 7
    assert current["intended_met"] == snapshot["intended_met"]
    observed = [(row["id"], row["intended_met"], row["text"]) for row in current["cases"]]
    recorded = [(row["id"], row["intended_met"], row["text"]) for row in snapshot["cases"]]
    assert observed == recorded


def test_holdout_misses_stay_visible():
    snapshot = json.loads((ROOT / "evals" / "holdout_observed.json").read_text(encoding="utf-8"))
    misses = [row["id"] for row in snapshot["cases"] if not row["intended_met"]]
    assert misses == ["holdout-negation-only", "holdout-usd-prefix"]
    assert snapshot["intended_met"] == 5
    assert snapshot["attempted"] == 7
