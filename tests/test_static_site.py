"""A static build can be hosted later. This test does not deploy it."""

import json
from pathlib import Path

from grave_truth.health import HEALTH_BODY
from grave_truth.static_site import build

ROOT = Path(__file__).resolve().parents[1]


def test_static_build_copies_the_health_body_and_the_letter(tmp_path):
    build(tmp_path)
    assert (tmp_path / "health").read_bytes() == HEALTH_BODY
    assert (tmp_path / "health.json").read_bytes() == HEALTH_BODY
    health = json.loads(HEALTH_BODY)
    assert health["live_model"] == "unimplemented"
    letter = (tmp_path / "grave-truth-dispute-letter.md").read_text(encoding="utf-8")
    clauses = (tmp_path / "grave-truth-clause-issues.md").read_text(encoding="utf-8")
    assert "not found" in letter.lower()
    assert "not found" in clauses.lower()
    judge = (tmp_path / "judge.html").read_text(encoding="utf-8")
    assert 'id="hero"' in judge
    assert "not found" in judge.lower()
    assert "$42.15" in judge
    assert "api_key" not in judge
    page = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert 'id="hero"' in page
    assert 'href="kiro.html"' in page
    kiro = (tmp_path / "kiro.html").read_text(encoding="utf-8")
    assert "0 of 17" in kiro
    assert "17 of 17" in kiro
    assert "Kiro IDE" in kiro
    for banned in ("Antler", "Americanas", "DocMinds", "Harbor", "Broadway", "2121"):
        assert banned not in kiro
    committed = ROOT / "site"
    assert (committed / "health").read_bytes() == (tmp_path / "health").read_bytes()
    assert (committed / "judge.html").read_text(encoding="utf-8") == judge
    assert (committed / "grave-truth-dispute-letter.md").read_text(encoding="utf-8") == letter
    assert (committed / "kiro.html").read_text(encoding="utf-8") == kiro
    assert (committed / "index.html").read_text(encoding="utf-8") == page
