"""One URL runs the synthetic sample. /health does not call a model."""

import importlib.util
import json
import threading
from http.client import HTTPConnection
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _server():
    path = ROOT / "demos" / "haunted" / "server.py"
    spec = importlib.util.spec_from_file_location("haunted_server_judge", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_health_is_static_and_names_the_missing_model():
    server = _server()
    first = server.route("GET", "/health", b"")
    second = server.route("GET", "/health?judge=1", b"")
    assert first == second
    status, content_type, data = first
    assert status == 200
    assert content_type.startswith("application/json")
    body = json.loads(data)
    assert body == {
        "status": "ok",
        "service": "grave-truth",
        "mode": "offline",
        "live_model": "unimplemented",
        "auth": "none",
    }
    assert "key" not in data.decode("utf-8").lower()


def test_export_route_matches_the_library_and_can_be_downloaded():
    server = _server()
    status, content_type, data = server.route("GET", "/api/export?app=eob", b"")
    assert status == 200
    assert "application/json" in content_type
    payload = json.loads(data)
    again = json.loads(server.route("GET", "/api/export?app=eob", b"")[2])
    assert payload == again
    assert payload["kind"] == "dispute-letter"
    assert payload["live_model"] == "unimplemented"
    md_status, md_type, md = server.route("GET", "/api/export?app=eob&format=markdown", b"")
    assert md_status == 200
    assert "markdown" in md_type
    assert md.decode("utf-8") == payload["markdown"]
    lease_status, _, lease = server.route("GET", "/api/export?app=lease&format=markdown", b"")
    assert lease_status == 200
    assert b"clause" in lease.lower()
    missing = server.route("GET", "/api/export?app=paste", b"")
    assert missing[0] == 400


def test_health_over_http_and_markdown_download_header():
    server = _server()
    httpd = server.make_server(0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address
    try:
        health = HTTPConnection(host, port, timeout=5)
        health.request("GET", "/health")
        response = health.getresponse()
        body = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert body["status"] == "ok"
        assert body["live_model"] == "unimplemented"
        health.close()

        export = HTTPConnection(host, port, timeout=5)
        export.request("GET", "/api/export?app=lease&format=markdown")
        downloaded = export.getresponse()
        text = downloaded.read().decode("utf-8")
        disposition = downloaded.getheader("Content-Disposition")
        assert downloaded.status == 200
        assert disposition == 'attachment; filename="grave-truth-clause-issues.md"'
        assert "not found" in text.lower()
        export.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_judge_query_runs_the_sample_without_a_second_click():
    html = (ROOT / "demos" / "haunted" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "demos" / "haunted" / "app.js").read_text(encoding="utf-8")
    assert 'id="hero"' in html
    assert 'id="artifact"' in html
    assert "Download" in html
    assert 'get("judge") === "1"' in script
    assert "runJudge" in script
    assert "/api/export?app=eob" in script
    assert "/api/ask" in script
    submit = script.split('form.addEventListener("submit"')[1].split("form.addEventListener")[0]
    assert "runJudge" not in submit
    load = script.split("renderPresets();")[-1]
    assert 'get("judge") === "1"' in load
    assert "runJudge();" in load
    lowered = script.lower()
    assert "api_key" not in lowered
    assert "apikey" not in lowered
    assert "openai" not in lowered
    assert "bearer " not in lowered
