"""The first screen says what the check does: input, check, result."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_hero_states_the_check_in_one_screen():
    html = (ROOT / "demos" / "haunted" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "demos" / "haunted" / "style.css").read_text(encoding="utf-8")
    start = html.index('id="hero"')
    hero = html[start:html.index("</header>", start)]
    assert "Input" in hero
    assert "Check" in hero
    assert "Result" in hero
    assert "not found" in hero.lower()
    assert "$42.15" in hero
    assert "dispute letter" in hero.lower() or "letter" in hero.lower()
    assert "prefers-reduced-motion" in css
    assert ".hero" in css
