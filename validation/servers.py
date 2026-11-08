"""Start the local demo and the one-file negative fixture."""

from __future__ import annotations

import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def start_product_server(root: Path, script: str) -> tuple[subprocess.Popen, str]:
    proc = subprocess.Popen(
        [sys.executable, script, "--port", "0"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    ready: list[str] = []
    log: list[str] = []
    started = threading.Event()

    def drain() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            log.append(line)
            if "http://127.0.0.1:" in line and not ready:
                ready.append(line.strip().split("http://", 1)[1])
                started.set()

    threading.Thread(target=drain, daemon=True).start()
    if not started.wait(timeout=10):
        stop_process(proc)
        tail = "".join(log)[-500:]
        raise RuntimeError(f"product server did not print a local URL. {tail}")
    host_port = ready[0].split("/", 1)[0]
    return proc, f"http://{host_port}/"


def stop_process(proc: subprocess.Popen | None) -> None:
    if proc is None or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)


class FixtureServer:
    def __init__(self, html: bytes):
        handler = _handler(html)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        host, port = self.httpd.server_address
        return f"http://{host}:{port}/"

    def start(self) -> str:
        self.thread.start()
        return self.url

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()


def _handler(html: bytes):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            path = self.path.split("?", 1)[0]
            if path in {"/", "/index.html"}:
                body = html
                status = 200
                content_type = "text/html; charset=utf-8"
            else:
                body = b"not found"
                status = 404
                content_type = "text/plain; charset=utf-8"
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt: str, *args) -> None:
            return

    return Handler
