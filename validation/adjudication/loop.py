"""Bounded evaluator-versus-critic loop. Default path is a scripted fixture, not a live model."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from validation.adjudication.judges import live_adapter_status, scripted_critic, scripted_evaluator
from validation.adjudication.repair import apply_set_bool, propose_is_safe
from validation.adjudication.rubric import criterion_rows, load_rubric

MAX_ROUNDS = 3
MAX_SECONDS = 5.0
PACKAGE = Path(__file__).resolve().parent
FIXTURES = PACKAGE / "fixtures"
PRIORS = PACKAGE.parent / "seeds" / "priors.json"

EXPECTED_STOPS = {
    "repair_demo": "improved_and_clear",
    "no_improvement": "no_improvement",
    "malformed": "malformed_judge_output",
    "unsupported": "unsupported_critique",
    "missing_rubric": "missing_rubric",
    "protected": "protected_submission",
    "unsafe": "unsafe_repair",
    "failed_blocks_ready": "failed_checks_block_ready",
}


def check_candidate(data: dict) -> list[dict]:
    focusable = data.get("focusable") is True
    return [{
        "id": "skip_target_focusable",
        "ok": focusable,
        "detail": "skip target can take focus" if focusable else "skip target cannot take focus",
    }]


def run_scenario(name: str, workspace: Path, *, env: dict | None = None) -> dict:
    if name not in EXPECTED_STOPS:
        raise ValueError(f"unknown scenario {name}")
    workspace.mkdir(parents=True, exist_ok=True)
    source = FIXTURES / ("frozen_candidate.json" if name == "protected" else "unfocusable_candidate.json")
    target = workspace / "candidate.json"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    rubric_path = None if name == "missing_rubric" else FIXTURES / "kiroween_2026_rubric.json"
    return run_loop(
        workspace,
        rubric_path,
        judge_mode=_mode(name),
        env=env or {},
        scenario=name,
    )


def run_all_scenarios(root: Path, *, env: dict | None = None) -> dict:
    base = root / "validation" / "adjudication" / "workspace" / "scenarios"
    results = []
    for name in EXPECTED_STOPS:
        result = run_scenario(name, base / name, env=env)
        results.append({
            "scenario": name,
            "stop": result["stop"]["reason"],
            "expected_stop": EXPECTED_STOPS[name],
            "matched": result["stop"]["reason"] == EXPECTED_STOPS[name],
            "repairs_accepted": len(result["repairs_accepted"]),
            "live_loop_validated": result["live_adapter"]["live_loop_validated"],
        })
    return {
        "kind": "scripted_fixture_simulation",
        "live_loop_validated": False,
        "scenarios": results,
        "ok": all(item["matched"] for item in results),
    }


def run_loop(workspace: Path, rubric_path: Path | None, *, judge_mode: str, env: dict, scenario: str) -> dict:
    started = time.monotonic()
    rubric = load_rubric(rubric_path)
    priors = _load_priors()
    live = live_adapter_status(env)
    candidate = workspace / "candidate.json"
    before_hash = _hash(candidate)
    protected_before = _protected_hashes()
    audit: dict = {
        "scenario": scenario,
        "kind": "scripted_fixture_simulation",
        "not_live_llm": True,
        "live_adapter": live,
        "priors_are_not_rules": True,
        "rubric_criteria": criterion_rows(rubric) if rubric else [],
        "rounds": [],
        "repairs_accepted": [],
        "repairs_rejected": [],
        "stop": {"reason": ""},
        "before_hash": before_hash,
        "after_hash": before_hash,
        "protected_hashes_unchanged": True,
    }
    if rubric is None:
        return _finish(audit, candidate, protected_before, "missing_rubric", started)
    data = json.loads(candidate.read_text(encoding="utf-8"))
    if data.get("submission_state") == "submitted_frozen":
        return _finish(audit, candidate, protected_before, "protected_submission", started)
    seen_repairs: list[str] = []
    previous_failed: tuple[str, ...] | None = None
    for round_index in range(1, MAX_ROUNDS + 1):
        if time.monotonic() - started > MAX_SECONDS:
            return _finish(audit, candidate, protected_before, "time_ceiling", started)
        data = json.loads(candidate.read_text(encoding="utf-8"))
        checks = check_candidate(data)
        failed = tuple(check["id"] for check in checks if not check["ok"])
        packet = {"checks": checks, "judge_mode": judge_mode, "priors": priors, "round": round_index}
        evaluator = scripted_evaluator(packet)
        critic = scripted_critic(packet)
        parsed_eval, eval_error = _parse_review(evaluator, "evaluator_simulation")
        parsed_critic, critic_error = _parse_review(critic, "critic_simulation")
        round_row = {
            "round": round_index,
            "checks": checks,
            "evaluator": evaluator if eval_error is None else {"rejected": eval_error},
            "critic": critic if critic_error is None else {"rejected": critic_error},
        }
        audit["rounds"].append(round_row)
        if eval_error or critic_error:
            return _finish(audit, candidate, protected_before, "malformed_judge_output", started)
        if judge_mode == "unsupported":
            audit["repairs_rejected"].append({"reason": "unsupported_critique", "claim": parsed_critic[0]["claim"]})
            return _finish(audit, candidate, protected_before, "unsupported_critique", started)
        if judge_mode == "subjective_pass":
            return _finish(audit, candidate, protected_before, "failed_checks_block_ready", started, checks)
        if not failed:
            return _finish(audit, candidate, protected_before, "improved_and_clear", started, checks)
        if previous_failed is not None and failed == previous_failed and seen_repairs:
            return _finish(audit, candidate, protected_before, "no_improvement", started, checks)
        proposal = _evidenced_repair(parsed_eval, parsed_critic, checks)
        if proposal is None:
            if judge_mode == "unsafe":
                rejected = _first_repair(parsed_eval)
                audit["repairs_rejected"].append({"reason": "unsafe_repair", "proposal": rejected})
                return _finish(audit, candidate, protected_before, "unsafe_repair", started, checks)
            return _finish(audit, candidate, protected_before, "failed_checks_block_ready", started, checks)
        safe, why = propose_is_safe(proposal, workspace)
        if not safe:
            audit["repairs_rejected"].append({"reason": why, "proposal": proposal})
            stop = "unsafe_repair" if why in {"unsafe_command", "unsafe_path", "protected_file"} else "no_improvement"
            return _finish(audit, candidate, protected_before, stop, started, checks)
        signature = json.dumps(proposal, sort_keys=True)
        if signature in seen_repairs:
            return _finish(audit, candidate, protected_before, "cycle", started, checks)
        before_bytes = candidate.read_bytes()
        applied, apply_reason = apply_set_bool(workspace, proposal)
        if not applied:
            audit["repairs_rejected"].append({"reason": apply_reason, "proposal": proposal})
            return _finish(audit, candidate, protected_before, "unsafe_repair", started, checks)
        retest = check_candidate(json.loads(candidate.read_text(encoding="utf-8")))
        retest_failed = tuple(check["id"] for check in retest if not check["ok"])
        if retest_failed == failed:
            candidate.write_bytes(before_bytes)
            audit["repairs_rejected"].append({"reason": "no_improvement", "proposal": proposal, "reverted": True})
            return _finish(audit, candidate, protected_before, "no_improvement", started, retest)
        seen_repairs.append(signature)
        audit["repairs_accepted"].append({
            "reason": "failed check cited by both simulations",
            "proposal": proposal,
            "before_failed": list(failed),
            "after_failed": list(retest_failed),
        })
        previous_failed = failed
        round_row["retest"] = retest
    return _finish(audit, candidate, protected_before, "max_rounds", started)


def _mode(scenario: str) -> str:
    return {
        "repair_demo": "repair",
        "no_improvement": "no_improvement",
        "malformed": "malformed",
        "unsupported": "unsupported",
        "missing_rubric": "repair",
        "protected": "repair",
        "unsafe": "unsafe",
        "failed_blocks_ready": "subjective_pass",
    }[scenario]


def _parse_review(review: dict | list, role: str) -> tuple[list[dict], str | None]:
    if not isinstance(review, dict):
        return [], "not_an_object"
    judgments = review.get("judgments")
    if not isinstance(judgments, list) or not judgments:
        return [], "judgments_not_a_list"
    parsed = []
    for item in judgments:
        if not isinstance(item, dict):
            return [], "judgment_not_an_object"
        if item.get("label") != "simulation" or item.get("role") != role:
            return [], "not_labeled_simulation"
        if not isinstance(item.get("evidence_refs"), list):
            return [], "evidence_refs_missing"
        parsed.append(item)
    return parsed, None


def _evidenced_repair(evaluator: list[dict], critic: list[dict], checks: list[dict]) -> dict | None:
    failed = {check["id"] for check in checks if not check["ok"]}
    evidence = {f"check:{check['id']}" for check in checks}
    for item in evaluator:
        repair = item.get("proposed_repair")
        refs = item.get("evidence_refs") or []
        if not repair or not refs:
            continue
        if any(ref not in evidence for ref in refs):
            continue
        if not any(ref.removeprefix("check:") in failed for ref in refs):
            continue
        critic_supports = any(
            set(other.get("evidence_refs") or []) & set(refs) and other.get("proposed_repair") is None
            for other in critic
        )
        critic_objects = any(
            other.get("proposed_repair") and not (other.get("evidence_refs") or [])
            for other in critic
        )
        if critic_objects and not critic_supports:
            continue
        if not critic_supports and critic:
            # A critic that cites the same failed check is required. Silence is not agreement.
            continue
        return repair
    return None


def _first_repair(evaluator: list[dict]) -> dict | None:
    for item in evaluator:
        if item.get("proposed_repair"):
            return item["proposed_repair"]
    return None


def _finish(audit: dict, candidate: Path, protected_before: dict, reason: str, started: float, checks: list[dict] | None = None) -> dict:
    if checks is None and candidate.is_file():
        try:
            checks = check_candidate(json.loads(candidate.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            checks = []
    checks = checks or []
    audit["stop"] = {"reason": reason, "seconds": round(time.monotonic() - started, 4), "cost_usd_observed": 0}
    audit["after_hash"] = _hash(candidate) if candidate.is_file() else None
    audit["checks"] = checks
    audit["all_ok"] = bool(checks) and all(check["ok"] for check in checks)
    audit["protected_hashes_unchanged"] = _protected_hashes() == protected_before
    audit["ready"] = False
    if reason == "improved_and_clear" and audit["all_ok"]:
        audit["candidate_result"] = "checks_passed_after_repair"
    elif reason == "failed_checks_block_ready":
        audit["candidate_result"] = "not-ready"
    else:
        audit["candidate_result"] = "insufficient-evidence" if reason == "missing_rubric" else "not-ready"
    return audit


def _hash(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _protected_hashes() -> dict:
    root = PACKAGE.parents[2]
    paths = [
        root / "evals" / "holdout_cases.json",
        root / "evals" / "gold_cases.json",
        root / "validation" / "adjudication" / "fixtures" / "kiroween_2026_rubric.json",
    ]
    return {str(path.relative_to(root)): _hash(path) for path in paths}


def _load_priors() -> dict:
    if not PRIORS.is_file():
        return {"priors": [], "missing": True}
    data = json.loads(PRIORS.read_text(encoding="utf-8"))
    data["used_as_rules"] = False
    return data
