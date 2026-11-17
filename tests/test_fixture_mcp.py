"""Keyless MCP: two synthetic fixtures, and nothing else."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read_message(stream) -> dict:
    headers = {}
    while True:
        line = stream.readline()
        if line in (b"\r\n", b"\n", b""):
            break
        key, value = line.decode("utf-8").split(":", 1)
        headers[key.strip().lower()] = value.strip()
    length = int(headers["content-length"])
    return json.loads(stream.read(length))


def _send(stream, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    stream.write(f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8") + body)
    stream.flush()


def _call(proc, name: str, arguments: dict) -> dict:
    _send(
        proc.stdin,
        {
            "jsonrpc": "2.0",
            "id": name,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
    )
    return _read_message(proc.stdout)


def test_fixture_mcp_returns_the_bill_and_refuses_other_paths():
    proc = subprocess.Popen(
        [sys.executable, str(ROOT / "scripts" / "fixture_mcp.py")],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    assert proc.stdin and proc.stdout
    try:
        _send(
            proc.stdin,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "grave-truth-test", "version": "0"},
                },
            },
        )
        init = _read_message(proc.stdout)
        assert init["id"] == 1
        assert "serverInfo" in init["result"]
        _send(proc.stdin, {"jsonrpc": "2.0", "method": "notifications/initialized"})
        listed = _call(proc, "list_synthetic_documents", {})
        names = listed["result"]["documents"]
        assert names == ["sample-eob", "sample-lease"]
        read = _call(proc, "read_synthetic_document", {"name": "sample-eob"})
        text = read["result"]["text"]
        expected = (ROOT / "fixtures" / "sample_eob.txt").read_text(encoding="utf-8")
        assert text == expected
        assert read["result"]["bytes"] == len(expected.encode("utf-8"))
        refused = _call(proc, "read_synthetic_document", {"name": "../README.md"})
        assert refused["result"]["bytes"] == 0
        assert refused["result"]["text"] == ""
        assert refused["result"]["error"]
        unknown = _call(proc, "read_synthetic_document", {"name": "sample-eob.txt"})
        assert unknown["result"]["bytes"] == 0
    finally:
        proc.kill()
        proc.wait(timeout=5)
