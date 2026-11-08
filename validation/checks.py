"""Assertions shared by scripted journeys. These are not model judgments."""

from __future__ import annotations


def mark_support(mark_texts: list[str], *, require: list[str], forbid: list[str] | None = None) -> dict:
    """A citation check passes only when every required phrase is in some mark."""
    forbid = forbid or []
    joined = "\n".join(mark_texts)
    missing = [phrase for phrase in require if phrase not in joined]
    forbidden_hits = [phrase for phrase in forbid if phrase in joined]
    ok = not missing and not forbidden_hits and (bool(mark_texts) if require else True)
    return {
        "ok": ok,
        "missing": missing,
        "forbidden_hits": forbidden_hits,
        "mark_count": len(mark_texts),
        "marks": mark_texts,
    }


def marks_are_document_slices(mark_texts: list[str], document: str) -> dict:
    """Every highlighted string must be copied from the pasted document."""
    if not mark_texts:
        return {"ok": False, "missing_slice": True, "outside": []}
    outside = [mark for mark in mark_texts if mark not in document]
    return {"ok": not outside, "missing_slice": False, "outside": outside}
