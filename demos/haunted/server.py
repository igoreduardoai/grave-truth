#!/usr/bin/env python3
"""Offline haunted demo. Stdlib HTTP server bound to 127.0.0.1.

Answers come from DocumentAgent and the synthetic fixtures. No model API
and no outbound requests. Uncited claims are ghosts. Cited answers carry
the source span offsets the page highlights.

    python3 demos/haunted/server.py
"""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from grave_truth.apps import eob, lease  # noqa: E402

HERE = Path(__file__).resolve().parent
HOST = "127.0.0.1"
DEFAULT_PORT = 8765
MAX_BODY = 8192

STATIC = {
    "/": "index.html",
    "/index.html": "index.html",
    "/app.js": "app.js",
    "/style.css": "style.css",
}
CONTENT_TYPES = {
    "index.html": "text/html; charset=utf-8",
    "app.js": "text/javascript; charset=utf-8",
    "style.css": "text/css; charset=utf-8",
}
APP_LABELS = {"eob": "eob-explainer", "lease": "lease-checker"}
DOC_IDS = {"eob": "sample-eob", "lease": "sample-lease"}


def _load(app: str):
    if app == "eob":
        return eob.load_agent()
    if app == "lease":
        return lease.load_agent()
    raise ValueError(f"unknown app {app}")


def _document(app: str) -> str:
    fixture = eob.FIXTURE if app == "eob" else lease.FIXTURE
    return fixture.read_text(encoding="utf-8")


def _citations(result) -> list[dict]:
    return [
        {
            "doc_id": citation.doc_id,
            "start": citation.start,
            "end": citation.end,
            "span": citation.span,
        }
        for citation in result.citations
    ]


def ask_payload(payload: dict) -> dict:
    """Run one local question or claim. Raises ValueError on a bad request."""
    app = payload.get("app")
    if app not in APP_LABELS:
        raise ValueError("app must be eob or lease")
    question = payload.get("question")
    if not isinstance(question, str):
        raise ValueError("question must be a string")
    question = question.strip()
    if not question:
        raise ValueError("question is required")
    if len(question) > 1000:
        raise ValueError("question is too long")
    mode = payload.get("mode") or "answer"
    if mode not in {"answer", "reject"}:
        raise ValueError("mode must be answer or reject")

    agent = _load(app)
    document = _document(app)
    if mode == "reject":
        rejected = agent.reject_ungrounded_claim(question)
        if rejected:
            return {
                "app": app,
                "app_label": APP_LABELS[app],
                "mode": mode,
                "question": question,
                "verdict": "rejected",
                "ghost": True,
                "answer": "rejected",
                "document_id": DOC_IDS[app],
                "document": document,
                "citations": [],
            }
        result = agent.answer(question)
        return {
            "app": app,
            "app_label": APP_LABELS[app],
            "mode": mode,
            "question": question,
            "verdict": "accepted",
            "ghost": False,
            "answer": result.text if result.found else "accepted",
            "document_id": DOC_IDS[app],
            "document": document,
            "citations": _citations(result) if result.found else [],
        }

    result = agent.answer(question)
    return {
        "app": app,
        "app_label": APP_LABELS[app],
        "mode": mode,
        "question": question,
        "verdict": "cited" if result.found else "not_found",
        "ghost": result.ghost,
        "answer": result.text,
        "document_id": DOC_IDS[app],
        "document": document,
        "citations": _citations(result),
    }


def document_payload(app: str) -> dict:
    if app not in APP_LABELS:
        raise ValueError("app must be eob or lease")
    return {
        "app": app,
        "app_label": APP_LABELS[app],
        "document_id": DOC_IDS[app],
        "document": _document(app),
    }


def route(method: str, path: str, body: bytes) -> tuple[int, str, bytes]:
    """Return status, content type, and body for one local request."""
    clean = path.split("?", 1)[0]
    if method == "GET" and clean in STATIC:
        name = STATIC[clean]
        data = (HERE / name).read_bytes()
        return 200, CONTENT_TYPES[name], data
    if method == "GET" and clean == "/api/document":
        query = {}
        if "?" in path:
            for part in path.split("?", 1)[1].split("&"):
                if "=" in part:
                    key, value = part.split("=", 1)
                    query[key] = value
        try:
            payload = document_payload(query.get("app", ""))
        except ValueError as exc:
            return _error(400, str(exc))
        return _json(200, payload)
    if method == "POST" and clean == "/api/ask":
        if len(body) > MAX_BODY:
            return _error(400, "body is too large")
        try:
            payload = json.loads(body.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("body must be a JSON object")
            result = ask_payload(payload)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            message = "body must be JSON" if isinstance(exc, (UnicodeDecodeError, json.JSONDecodeError)) else str(exc)
            return _error(400, message)
        return _json(200, result)
    return _error(404, "not found")


def _json(status: int, payload: dict) -> tuple[int, str, bytes]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return status, "application/json; charset=utf-8", data


def _error(status: int, message: str) -> tuple[int, str, bytes]:
    return _json(status, {"error": message})


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        self._respond("GET", b"")

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or "0")
        if length > MAX_BODY:
            status, content_type, data = _error(400, "body is too large")
            self._write(status, content_type, data)
            return
        body = self.rfile.read(length) if length else b""
        self._respond("POST", body)

    def _respond(self, method: str, body: bytes) -> None:
        status, content_type, data = route(method, self.path, body)
        self._write(status, content_type, data)

    def _write(self, status: int, content_type: str, data: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def make_server(port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((HOST, port), Handler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the offline haunted Grave Truth demo.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args(argv)
    try:
        server = make_server(args.port)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    host, port = server.server_address
    print(f"Haunted demo at http://{host}:{port}/", flush=True)
    print("Local only. Synthetic fixtures. Not a medical device and not legal advice.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
