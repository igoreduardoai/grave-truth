"""Block Kiro hook writes that target secret-looking paths. No network calls."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_PATH_KEYS = {
    "path",
    "filepath",
    "file_path",
    "uri",
    "target",
    "target_file",
    "filename",
    "file",
}
_EXACT_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "id_rsa",
    "id_dsa",
    "credentials.json",
    "secrets.json",
}
_SUFFIXES = (".pem", ".p12", ".key")


def find_secret_paths(payload: str) -> list[str]:
    """Return secret-looking paths named in a hook payload. Empty if unsure."""
    if not payload.strip():
        return []
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return []
    found: list[str] = []
    for candidate in _walk_paths(data):
        if _is_secret(candidate) and candidate not in found:
            found.append(candidate)
    return found


def main() -> int:
    payload = sys.stdin.read()
    secrets = find_secret_paths(payload)
    if not secrets:
        return 0
    print(
        "blocked: refusing to touch secret-looking paths: " + ", ".join(secrets),
        file=sys.stderr,
    )
    return 2


def _walk_paths(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(key, str) and key.lower() in _PATH_KEYS and isinstance(value, str):
                found.append(value)
            else:
                found.extend(_walk_paths(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_walk_paths(item))
    return found


def _is_secret(path: str) -> bool:
    name = Path(path).name.lower()
    if name in _EXACT_NAMES or name.startswith(".env"):
        return True
    if name.endswith(_SUFFIXES):
        return True
    parts = {part.lower() for part in Path(path).parts}
    return "secrets" in parts
