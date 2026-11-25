"""Ready, not-ready, or insufficient-evidence. No score and no prize claim."""

from __future__ import annotations


def decide(config: dict, facts: dict) -> dict:
    """Use the app's configured requirements. Manual items are never auto-approved."""
    readiness = config.get("readiness") or {}
    mandatory = list(readiness.get("mandatory") or [])
    manual = list(readiness.get("manual") or [])
    reasons = []
    skipped = []
    failed = []
    for name in mandatory:
        layer = facts.get("layers", {}).get(name) or {}
        status = layer.get("status")
        if status in {None, "skipped"} or layer.get("exercised") is False:
            skipped.append(name)
        elif status == "failed" or layer.get("ok") is False:
            failed.append(name)
    if facts.get("holdout", {}).get("intended_met") != facts.get("holdout", {}).get("attempted"):
        reasons.append("held-out intended behavior was not met on every case")
    unresolved = list(facts.get("unresolved") or [])
    manual_open = [item for item in manual if not (config.get("manual_approvals") or {}).get(item)]
    if skipped or failed:
        decision = "not-ready"
        if skipped:
            reasons.append("mandatory checks skipped: " + ", ".join(skipped))
        if failed:
            reasons.append("mandatory checks failed: " + ", ".join(failed))
    elif manual_open or unresolved or reasons:
        decision = "insufficient-evidence"
        if manual_open:
            reasons.append("manual checks are not approved: " + ", ".join(manual_open))
        if unresolved:
            reasons.append("unresolved evidence: " + "; ".join(unresolved))
    else:
        decision = "ready"
        reasons.append("configured mandatory checks passed and manual approvals are recorded")
    return {
        "decision": decision,
        "reasons": reasons,
        "mandatory_skipped": skipped,
        "mandatory_failed": failed,
        "manual_open": manual_open,
        "not_a_prize_claim": True,
        "not_a_score": True,
    }
