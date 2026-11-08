"""Allowlisted edits inside one workspace. No shell and no path escape."""

from __future__ import annotations

import json
from pathlib import Path

ALLOWED_REPAIRS = {
    "skip_target_focusable": {"key": "focusable", "value": True},
    "record_note": {"key": "note", "value": "reviewed"},
}

PROTECTED_NAMES = {
    "holdout_cases.json",
    "holdout_observed.json",
    "gold_cases.json",
    "kiroween_2026_rubric.json",
    "adversarial_cases.json",
}


def contained(workspace: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(workspace.resolve())
    except ValueError:
        return False
    return True


def propose_is_safe(proposal: dict, workspace: Path) -> tuple[bool, str]:
    if not isinstance(proposal, dict):
        return False, "malformed_proposal"
    if any(key in proposal for key in ("command", "exec", "shell", "argv")):
        return False, "unsafe_command"
    if proposal.get("op") != "set_bool":
        return False, "op_not_allowlisted"
    check_id = proposal.get("check_id")
    if check_id not in ALLOWED_REPAIRS:
        return False, "check_not_repairable"
    raw_path = proposal.get("path") or "candidate.json"
    if not isinstance(raw_path, str) or raw_path.startswith(("/", "\\")) or ".." in Path(raw_path).parts:
        return False, "unsafe_path"
    target = (workspace / raw_path).resolve()
    if not contained(workspace, target):
        return False, "unsafe_path"
    if target.name in PROTECTED_NAMES:
        return False, "protected_file"
    return True, "allowlisted"


def apply_set_bool(workspace: Path, proposal: dict) -> tuple[bool, str]:
    safe, reason = propose_is_safe(proposal, workspace)
    if not safe:
        return False, reason
    target = (workspace / (proposal.get("path") or "candidate.json")).resolve()
    if not target.is_file():
        return False, "missing_candidate"
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return False, "malformed_candidate"
    spec = ALLOWED_REPAIRS[proposal["check_id"]]
    data[spec["key"]] = spec["value"]
    target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True, "applied"
