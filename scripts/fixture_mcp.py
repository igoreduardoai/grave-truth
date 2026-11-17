#!/usr/bin/env python3
"""Keyless MCP server for the two synthetic fixtures.

Speaks MCP over stdio with Content-Length framing. It reads two files in
fixtures/ and refuses every other name. It does not open a network socket
and it does not read an API key.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW = {
    "sample-eob": ROOT / "fixtures" / "sample_eob.txt",
    "sample-lease": ROOT / "fixtures" / "sample_lease.txt",
}


def _read() -> dict | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if line == b"":
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, value = line.decode("utf-8").split(":", 1)
        headers[key.strip().lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    return json.loads(sys.stdin.buffer.read(length))


def _write(payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8") + body)
    sys.stdout.buffer.flush()


def _reply(message: dict, result: dict) -> None:
    _write({"jsonrpc": "2.0", "id": message.get("id"), "result": result})


def _read_document(name: object) -> dict:
    if not isinstance(name, str) or name not in ALLOW:
        return {"text": "", "bytes": 0, "error": "unknown document"}
    text = ALLOW[name].read_text(encoding="utf-8")
    return {"text": text, "bytes": len(text.encode("utf-8")), "error": ""}


def _call(params: dict) -> dict:
    name = params.get("name")
    arguments = params.get("arguments") or {}
    if name == "list_synthetic_documents":
        documents = sorted(ALLOW)
        return {
            "documents": documents,
            "content": [{"type": "text", "text": "\n".join(documents)}],
        }
    if name == "read_synthetic_document":
        found = _read_document(arguments.get("name"))
        return {
            **found,
            "content": [{"type": "text", "text": found["text"]}],
            "isError": bool(found["error"]),
        }
    return {"text": "", "bytes": 0, "error": "unknown tool", "isError": True}


def main() -> int:
    while True:
        message = _read()
        if message is None:
            return 0
        method = message.get("method")
        if method == "notifications/initialized":
            continue
        if "id" not in message:
            continue
        if method == "initialize":
            _reply(
                message,
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "grave-truth-fixtures", "version": "0.1.0"},
                },
            )
            continue
        if method == "tools/list":
            _reply(
                message,
                {
                    "tools": [
                        {
                            "name": "list_synthetic_documents",
                            "description": "List the two synthetic fixture names. No other files are served.",
                            "inputSchema": {"type": "object", "properties": {}},
                        },
                        {
                            "name": "read_synthetic_document",
                            "description": "Read one synthetic fixture by its allowlisted name.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"name": {"type": "string"}},
                                "required": ["name"],
                            },
                        },
                    ]
                },
            )
            continue
        if method == "tools/call":
            _reply(message, _call(message.get("params") or {}))
            continue
        _reply(message, {"error": "unsupported method"})


if __name__ == "__main__":
    sys.exit(main())
