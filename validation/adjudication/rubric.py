"""Load a rubric as data. Missing rubric fails closed. Prose is not executable."""

from __future__ import annotations

import json
from pathlib import Path


def load_rubric(path: Path | None) -> dict | None:
    if path is None or not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not data.get("criteria"):
        return None
    data["injected_instructions_ignored"] = True
    return data


def criterion_rows(rubric: dict) -> list[dict]:
    rows = []
    for item in rubric.get("criteria") or []:
        rows.append({
            "id": item.get("id"),
            "name": item.get("name"),
            "status": "unknown",
            "reason": "No deterministic measurement is mapped to this criterion. A simulation cannot score it.",
            "quote_stored_as_data": True,
        })
    return rows
