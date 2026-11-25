"""Web demo: request JSON, pasted documents, and rejected empty or oversized input."""

import importlib.util
import json
import threading
from http.client import HTTPConnection
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load():
    path = ROOT / "demos" / "haunted" / "server.py"
    spec = importlib.util.spec_from_file_location("haunted_server_web", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _post(server, payload: dict) -> tuple[int, dict]:
    status, content_type, data = server.route(
        "POST",
        "/api/ask",
        json.dumps(payload).encode("utf-8"),
    )
    assert "application/json" in content_type
    return status, json.loads(data)


def test_pasted_document_question_returns_verdict_json():
    server = _load()
    document = (ROOT / "fixtures" / "sample_lease.txt").read_text(encoding="utf-8")
    status, payload = _post(
        server,
        {
            "app": "paste",
            "document": document,
            "question": "What is the security deposit?",
        },
    )
    assert status == 200
    assert payload["verdict"] == "cited"
    assert payload["ghost"] is False
    assert payload["document_id"] == "pasted-document"
    assert payload["document"] == document.strip()
    citation = payload["citations"][0]
    assert payload["document"][citation["start"]:citation["end"]] == citation["span"]
    assert "security deposit" in citation["span"]
    assert "$1,850.00" in citation["span"]
    assert "not rent" in citation["span"]


def test_proposed_answer_marks_cited_and_ghost_claims():
    server = _load()
    status, payload = _post(
        server,
        {
            "app": "eob",
            "answer": "The patient responsibility is $42.15. The pharmacy charge is $180.00.",
        },
    )
    assert status == 200
    assert payload["verdict"] == "mixed"
    assert payload["ghost"] is False
    assert [claim["ghost"] for claim in payload["claims"]] == [False, True]
    cited, ghost = payload["claims"]
    assert cited["verdict"] == "cited"
    assert "$42.15" in cited["citations"][0]["span"]
    assert "180.00" not in cited["citations"][0]["span"]
    assert ghost["verdict"] == "rejected"
    assert ghost["citations"] == []
    assert payload["citations"]
    assert all("$180.00" not in item["span"] for item in payload["citations"])
    for item in payload["citations"]:
        assert payload["document"][item["start"]:item["end"]] == item["span"]


def test_question_and_answer_both_use_the_library():
    server = _load()
    status, payload = _post(
        server,
        {
            "app": "lease",
            "question": "What is the security deposit?",
            "answer": "The late fee is $1,850.00. The late fee is $75.00.",
        },
    )
    assert status == 200
    asked = payload["question_result"]
    assert asked["verdict"] == "cited"
    assert asked["ghost"] is False
    assert "not rent" in asked["citations"][0]["span"]
    assert [claim["ghost"] for claim in payload["claims"]] == [True, False]
    assert "$75.00" in payload["claims"][1]["citations"][0]["span"]


def test_empty_question_answer_and_document_are_rejected():
    server = _load()
    missing_text = [
        {"app": "eob", "question": "   "},
        {"app": "eob"},
        {"app": "lease", "question": "", "answer": "  "},
    ]
    for payload in missing_text:
        status, body = _post(server, payload)
        assert status == 400, payload
        assert body["error"] == "question or answer is required"
    for payload in (
        {"app": "paste", "question": "What is the copay?", "document": " \n "},
        {"app": "paste", "answer": "The copay is $3.00.", "document": ""},
    ):
        status, body = _post(server, payload)
        assert status == 400, payload
        assert body["error"] == "document is required"


def test_oversized_body_and_document_are_rejected():
    server = _load()
    status, content_type, data = server.route("POST", "/api/ask", b"x" * (server.MAX_BODY + 1))
    assert status == 400
    assert "application/json" in content_type
    assert json.loads(data)["error"] == "body is too large"

    document = "Synthetic clause about a demo copay. " * ((server.MAX_DOCUMENT // 20) + 2)
    assert len(document) > server.MAX_DOCUMENT
    encoded = json.dumps(
        {"app": "paste", "document": document, "question": "What is the copay?"}
    ).encode("utf-8")
    assert len(encoded) <= server.MAX_BODY
    status, body = _post(server, json.loads(encoded))
    assert status == 400
    assert body["error"] == "document is too long"


def test_http_request_returns_verdict_and_rejects_oversized_length():
    server = _load()
    httpd = server.make_server(0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address
    try:
        connection = HTTPConnection(host, port, timeout=5)
        body = json.dumps(
            {
                "app": "paste",
                "document": "The gift shop sold a postcard for $1.25.",
                "question": "How much is the postcard?",
            }
        )
        connection.request("POST", "/api/ask", body=body, headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert payload["verdict"] == "cited"
        assert payload["ghost"] is False
        assert "$1.25" in payload["citations"][0]["span"]
        connection.close()

        oversized = HTTPConnection(host, port, timeout=5)
        oversized.request(
            "POST",
            "/api/ask",
            body=b"{}",
            headers={"Content-Type": "application/json", "Content-Length": str(server.MAX_BODY + 50)},
        )
        denied = oversized.getresponse()
        denied_body = json.loads(denied.read().decode("utf-8"))
        assert denied.status == 400
        assert denied_body["error"] == "body is too large"
        oversized.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_readme_documents_the_judge_quickstart():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Judge quickstart" in readme
    assert "python3 demos/haunted/server.py" in readme
    assert "127.0.0.1" in readme
    assert "DocumentAgent" in readme


def test_page_exposes_paste_pick_and_accessible_names():
    html = (ROOT / "demos" / "haunted" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "demos" / "haunted" / "style.css").read_text(encoding="utf-8")
    script = (ROOT / "demos" / "haunted" / "app.js").read_text(encoding="utf-8")
    assert "<fieldset" in html
    assert 'for="document"' in html
    assert 'for="question"' in html
    assert 'for="answer"' in html
    assert "Paste a document" in html
    assert "Sample EOB" in html
    assert "Sample lease" in html
    assert "prefers-reduced-motion" in css
    assert "focus-visible" in css
    assert "ghost-claim" in script
    assert "mark" in script
