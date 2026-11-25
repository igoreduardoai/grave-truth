"""Load one app's validation config. The file is the reusable per-app surface."""

from __future__ import annotations

import json
from pathlib import Path

from validation.allowlist import is_local_prefix

PACKAGE = Path(__file__).resolve().parent
ALLOWED_KINDS = frozenset({
    "scripted_profile",
    "negative_control",
    "adapter_test_double",
    "safety_probe",
})


def app_path(app_id: str) -> Path:
    return PACKAGE / "apps" / f"{app_id}.json"


def load_app(app_id: str) -> dict:
    path = app_path(app_id)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_app(data)
    if errors:
        raise ValueError(f"{path.name}: " + "; ".join(errors))
    data["_path"] = str(path)
    return data


def validate_app(data: dict) -> list[str]:
    errors: list[str] = []
    if not data.get("id"):
        errors.append("id is required")
    prefixes = data.get("allowlist") or []
    if not prefixes:
        errors.append("allowlist is required")
    for prefix in prefixes:
        if not is_local_prefix(prefix):
            errors.append(f"allowlist entry is not local: {prefix}")
    llm = data.get("llm") or {}
    if llm.get("opt_in") not in {True, False}:
        errors.append("llm.opt_in must be true or false")
    for profile in data.get("scripted_profiles") or []:
        errors.extend(_kind(profile, "scripted_profile"))
    for control in data.get("negative_controls") or []:
        errors.extend(_kind(control, "negative_control"))
    double = data.get("persona_double") or {}
    if double:
        errors.extend(_kind(double, "adapter_test_double"))
    probe = data.get("safety_probe") or {}
    if probe:
        errors.extend(_kind(probe, "safety_probe"))
    return errors


def _kind(item: dict, expected: str) -> list[str]:
    kind = item.get("kind")
    if kind != expected:
        return [f"{item.get('id', expected)} kind must be {expected}"]
    if kind not in ALLOWED_KINDS:
        return [f"kind {kind} is not allowed"]
    return []
