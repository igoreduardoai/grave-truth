"""The held-out file is compared with the recorded measurement. It is not an accuracy claim."""

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
    """Every held-out row stays in the snapshot. A miss cannot be dropped from the record."""
    current = measure(ROOT)
    snapshot = load_snapshot(ROOT)
    assert [row["id"] for row in snapshot["cases"]] == [row["id"] for row in current["cases"]]
    misses = [row["id"] for row in snapshot["cases"] if not row["intended_met"]]
    live = [row["id"] for row in current["cases"] if not row["intended_met"]]
    assert live == misses == []
    assert snapshot["intended_met"] == snapshot["attempted"] == 7
