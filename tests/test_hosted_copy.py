"""Hosted deployments must not claim the page is local-only; local runs keep that wording."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load():
    path = ROOT / "demos" / "haunted" / "server.py"
    spec = importlib.util.spec_from_file_location("haunted_server_hosted", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _page(server, path):
    status, _type, data = server.route("GET", path, b"")
    assert status == 200
    return data.decode("utf-8")


def test_local_run_keeps_local_wording(monkeypatch):
    monkeypatch.delenv("VERCEL", raising=False)
    monkeypatch.delenv("GRAVE_TRUTH_HOSTED", raising=False)
    server = _load()
    page = _page(server, "/")
    assert "local only" in page
    assert "Nothing is sent off this machine." in page
    assert "Hosted demo:" not in page


def test_hosted_run_replaces_every_local_only_claim(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    server = _load()
    page = _page(server, "/")
    script = _page(server, "/app.js")
    assert server.HOSTED_NOTICE in page
    assert "hosted demo" in page
    for text in (page, script):
        assert "local only" not in text
        assert "off this machine" not in text
        assert "stays on this machine" not in text
        assert "local library" not in text
        assert "local Python library" not in text


def test_every_hosted_anchor_exists():
    server = _load()
    for name, pairs in server.HOSTED_COPY.items():
        text = (server.HERE / name).read_text(encoding="utf-8")
        for old, _new in pairs:
            assert old in text, (name, old)
