"""The capability matrix page repeats the repository file and adds no claim."""

import importlib.util
from pathlib import Path

from grave_truth.matrix_page import render_matrix_document

ROOT = Path(__file__).resolve().parents[1]
BANNED = ("Antler", "Americanas", "DocMinds", "Harbor", "Broadway", "2121")


def _server():
    path = ROOT / "demos" / "haunted" / "server.py"
    spec = importlib.util.spec_from_file_location("haunted_server_matrix", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_matrix_page_keeps_the_measured_lines_and_adds_no_banned_token():
    source = (ROOT / "docs" / "KIRO-CAPABILITY-MATRIX.md").read_text(encoding="utf-8")
    page = render_matrix_document(source)
    for line in (
        "0 of 17",
        "17 of 17",
        "Kiro IDE",
        "did not record",
        "scripted simulations",
        "was not deployed",
    ):
        assert line in page
        assert line in source
    for banned in BANNED:
        assert banned not in page
    assert "<table>" in page
    assert 'lang="en"' in page


def test_server_serves_the_matrix_at_both_paths():
    server = _server()
    for path in ("/kiro", "/kiro.html"):
        status, content_type, data = server.route("GET", path, b"")
        assert status == 200
        assert content_type.startswith("text/html")
        text = data.decode("utf-8")
        assert "0 of 17" in text
        assert "unimplemented" not in text or "live model" in text.lower() or "A live model" in text
        for banned in BANNED:
            assert banned not in text
