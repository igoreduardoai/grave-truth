"""Playwright shots and the axe report produced with them."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"


def test_gallery_has_real_screenshots_and_axe_is_clean():
    shots = sorted(GALLERY.glob("*.png"))
    assert len(shots) >= 8
    for shot in shots:
        header = shot.read_bytes()[:8]
        assert header == b"\x89PNG\r\n\x1a\n"
        assert shot.stat().st_size > 1000
    report = json.loads((GALLERY / "axe-report.json").read_text(encoding="utf-8"))
    assert report["violations"] == 0
    assert report["tool"] == "axe-core"
    assert len(report["pages"]) >= 8
    for page in report["pages"]:
        assert page["violations"] == 0
        assert page["incomplete"] == 0
