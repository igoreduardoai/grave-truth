"""Vercel entry point. Wraps demos/haunted/server.py unchanged. Built from PR #9 head 2aa041f.

vercel.json rewrites every path to /api/index?__p=<path>. This class restores the
original path before the unchanged local router sees it.
"""
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "demos" / "haunted"))

from server import Handler  # noqa: E402


def _restore(raw: str) -> str:
    parts = urlsplit(raw)
    pairs = parse_qsl(parts.query, keep_blank_values=True)
    original = None
    rest = []
    for key, value in pairs:
        if key == "__p" and original is None:
            original = value
        else:
            rest.append((key, value))
    if original is None:
        return raw
    path = "/" + original.lstrip("/")
    return path + ("?" + urlencode(rest) if rest else "")


class handler(Handler):  # noqa: N801
    def _respond(self, method, body):
        self.path = _restore(self.path)
        super()._respond(method, body)
