"""Rules quotes and the gate self-check stay dated and do not invent a verdict."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_rules_check_quotes_the_official_page():
    text = (ROOT / "docs" / "KIROWEEN-RULES-CHECK.md").read_text(encoding="utf-8")
    assert "2026-11-17" in text
    assert "https://kiroween.devpost.com/rules" in text
    assert "Skeleton Crew: Build a skeleton code template" in text
    assert "open source license file" in text
    assert "/.kiro" in text
    assert "Do NOT add the /.kiro directory" in text
    assert "2 separate repo folders" in text
    assert "Potential Impact (20% - 10 points)" in text
    assert "Technological Implementation (20% - 10 points)" in text
    assert "Design (20% - 10 points)" in text
    assert "Innovation/Idea (20% - 10 points)" in text
    assert "Presentation (20% - 10 points)" in text
    assert "December 4, 2026 (2:00 pm Pacific Time)" in text
    assert "America/Chicago" in text
    assert "Updated November 16, 2026, to include residents of Australia." in text
    for banned in ("2121", "Broadway", "Harbor", "Americanas", "44 months", "21 cases"):
        assert banned not in text


def test_capability_matrix_records_the_measured_counts():
    text = (ROOT / "docs" / "KIRO-CAPABILITY-MATRIX.md").read_text(encoding="utf-8")
    assert "specs" in text.lower()
    assert "steering" in text.lower()
    assert "hook" in text.lower()
    assert "MCP" in text
    assert "0 of 17" in text
    assert "17 of 17" in text
    assert "4" in text
    assert "Kiro IDE" in text
    assert "did not record" in text.lower() or "not recorded" in text.lower()
    for banned in ("Americanas", "Harbor", "44 months", "21 cases", "2121", "Broadway"):
        assert banned not in text


def test_gate_self_check_leaves_the_human_items_open():
    text = (ROOT / "docs" / "GATE-SELF-CHECK-2026-11-17.md").read_text(encoding="utf-8")
    assert "self-check" in text.lower()
    assert "judge_stack" in text
    assert "was not executed" in text
    for item in ("B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        assert item in text
    assert "B7" in text and "needs-human" in text
    assert "video" in text.lower()
    for banned in ("Americanas", "Harbor", "44 months", "21 cases", "2121", "Broadway"):
        assert banned not in text


def test_readme_before_and_after_matches_the_new_tests():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Before and after" in text
    assert "?judge=1" in text
    assert "/health" in text
    assert "unimplemented" in text
    assert "simulation" in text.lower()
    assert "Kiro IDE" in text
    assert "python3 scripts/build_static.py" in text or "site/" in text
    for banned in ("Americanas", "DocMinds", "44 months", "21 cases", "Harbor", "2121", "Broadway"):
        assert banned not in text
