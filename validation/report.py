"""Report shape. There is no aggregate quality score."""

from __future__ import annotations

import json
from pathlib import Path


def summarize_profiles(profiles: list[dict]) -> dict:
    attempted = [item for item in profiles if item.get("kind") == "scripted_profile"]
    completed = [item for item in attempted if item.get("completed")]
    citation = [item for item in attempted if item.get("citation")]
    citation_correct = [item for item in citation if item.get("completed")]
    refusal = [item for item in attempted if item.get("refusal")]
    refusal_correct = [item for item in refusal if item.get("completed")]
    return {
        "tasks_completed": len(completed),
        "tasks_attempted": len(attempted),
        "citation_correct": len(citation_correct),
        "citation_applicable": len(citation),
        "refusal_correct": len(refusal_correct),
        "refusal_applicable": len(refusal),
    }


def confirmed_defects(profiles: list[dict]) -> list[dict]:
    defects = []
    for item in profiles:
        if item.get("kind") != "scripted_profile" or item.get("completed"):
            continue
        defects.append({
            "status": "confirmed",
            "category": item.get("category", "journey"),
            "task_id": item.get("id"),
            "detail": item.get("failure_detail") or "a scripted check failed",
        })
    return defects


def negative_control_caught(checks: list[dict]) -> bool:
    """The control works when the harness fails the planted bad page."""
    return any(not check.get("passed") for check in checks)


def build_report(parts: dict) -> dict:
    profiles = parts["scripted_profiles"]
    summary = summarize_profiles(profiles)
    report = {
        "stack": "grave-truth-pre-submission-validation",
        "app": parts["app_id"],
        "repo": parts.get("repo"),
        "mode": "local",
        "commit": parts["commit"],
        "date": parts["date"],
        "cost_usd_observed": 0,
        "model_api_calls": parts.get("model_api_calls", 0),
        "decision": parts.get("decision"),
        "versions": parts["versions"],
        "layers": parts["layers"],
        "holdout": parts.get("holdout"),
        "scripted_profiles": {
            **summary,
            "note": "Scripted Playwright profiles. Not LLM synthetic users.",
            "tasks": profiles,
        },
        "negative_controls": parts["negative_controls"],
        "confirmed_defects": confirmed_defects(profiles),
        "automated_rule_findings": parts.get("axe_findings") or [],
        "limitations": parts.get("limitations") or [],
        "ux_hypotheses": parts.get("ux_hypotheses") or [],
        "persona": parts["persona"],
        "note": "This report has no aggregate quality score and does not claim a prize.",
    }
    if "quality_score" in report:
        raise RuntimeError("quality_score must not be emitted")
    return report


def write_report(report: dict, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "observed.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (directory / "OBSERVED.md").write_text(render_markdown(report), encoding="utf-8")


def render_markdown(report: dict) -> str:
    profiles = report["scripted_profiles"]
    gold = report["layers"]["pytest_and_gold"]
    lines = [
        "# Observed validation run",
        "",
        f"- Date: {report['date']}",
        f"- Commit: `{report['commit']}`",
        f"- Mode: {report['mode']}",
        f"- Observed cost: ${report['cost_usd_observed']} (model API calls: {report['model_api_calls']})",
        f"- App config: `{report['app']}`",
        f"- Repo: {report.get('repo')}",
        "",
        "## Decision",
        "",
    ]
    decision = report.get("decision") or {}
    lines.append(f"- **{decision.get('decision', 'missing')}**")
    for reason in decision.get("reasons") or []:
        lines.append(f"- {reason}")
    lines.append("- Manual items are not treated as passed.")
    lines.append("- This is not a prize estimate and not a quality score.")
    lines.extend([
        "",
        "## Denominators",
        "",
        f"- Scripted tasks completed: {profiles['tasks_completed']} / {profiles['tasks_attempted']}",
        f"- Citation checks correct: {profiles['citation_correct']} / {profiles['citation_applicable']}",
        f"- Refusals correct: {profiles['refusal_correct']} / {profiles['refusal_applicable']}",
        "",
        "Scripted profiles are deterministic browser steps. They are not LLM synthetic users.",
        "",
        "## Pytest and gold",
        "",
        f"- pytest exit {gold['pytest']['exit_code']}: passed {gold['pytest']['passed']}, failed {gold['pytest']['failed'] or 0}",
        f"- gold exit {gold['gold']['exit_code']}: {gold['gold']['passed']}/{gold['gold']['total']}",
        "",
        "## Layers",
        "",
    ])
    for name, layer in report["layers"].items():
        status = layer.get("status") or ("ok" if layer.get("ok") else "not ok")
        lines.append(f"- {name}: {status}")
    lines.extend(["", "## axe-core", ""])
    axe = report["layers"].get("axe_core") or {}
    lines.append(f"- violations: {axe.get('violation_count')}")
    lines.append(f"- incomplete: {axe.get('incomplete_count')}")
    lines.append(f"- {axe.get('note')}")
    for state in axe.get("states") or []:
        for item in state.get("incomplete") or []:
            lines.append(
                f"- incomplete {item.get('id')} on {state.get('state')} "
                f"({item.get('node_count')} nodes): {item.get('help')}"
            )
        for item in state.get("violations") or []:
            lines.append(
                f"- violation {item.get('id')} on {state.get('state')} "
                f"({item.get('impact')}): {item.get('help')}"
            )
    light = report["layers"].get("lighthouse") or {}
    lines.extend(["", "## Lighthouse laboratory diagnostic", ""])
    if light.get("status") != "diagnostic":
        lines.append(f"- {light.get('status')}: {light.get('reason', '')}")
    else:
        lines.append(
            f"- Lighthouse {light.get('lighthouse_version')}, "
            f"form factor {light.get('form_factor')}, "
            f"throttling {light.get('throttling_method')}, "
            f"mobile emulation {light.get('screen_emulation_mobile')}"
        )
        metrics = light.get("metrics") or {}
        for key, value in metrics.items():
            lines.append(f"- {key}: {value}")
        for name, category in (light.get("lab_category_scores") or {}).items():
            lines.append(f"- lab category {name}: {category.get('lab_score')}")
        lines.append(f"- {light.get('note')}")
    lines.extend(["", "## Negative controls", ""])
    controls = report.get("negative_controls") or []
    caught = sum(1 for item in controls if item.get("caught"))
    lines.append(f"- Planted citation failures caught: {caught} / {len(controls)}")
    probe = (report.get("persona") or {}).get("safety_probe") or {}
    lines.append(f"- Off-allowlist click probe: {probe.get('status', 'not run')}")
    lines.extend(["", "## Holdout", ""])
    holdout = report.get("holdout") or {}
    lines.append(
        f"- Intended behavior met: {holdout.get('intended_met')} / {holdout.get('attempted')}"
    )
    for row in holdout.get("cases") or []:
        if not row.get("intended_met"):
            lines.append(f"- Miss {row.get('id')}: intended {row.get('intended')}; observed {row.get('text')}")
    lines.extend(["", "## Confirmed defects", ""])
    defects = report["confirmed_defects"]
    if not defects:
        lines.append("No scripted profile failed in this run.")
    else:
        for defect in defects:
            lines.append(f"- {defect['category']} / {defect['task_id']}: {defect['detail']}")
    lines.extend(["", "## Limitations and hypotheses", ""])
    if report["limitations"]:
        for item in report["limitations"]:
            lines.append(f"- Limitation: {item.get('detail')}")
    else:
        lines.append("- No extra limitations were recorded by the profiles.")
    if report["ux_hypotheses"]:
        for item in report["ux_hypotheses"]:
            lines.append(f"- UX hypothesis (not a confirmed defect): {item}")
    else:
        lines.append("- No UX hypotheses. The LLM persona runner was not exercised, so none were invented.")
    lines.extend(["", "## Persona", ""])
    persona = report["persona"]
    llm = persona["llm"]
    lines.append(f"- LLM runner: {llm.get('status')}. {llm.get('reason', '')}")
    double = persona.get("adapter_test_double") or {}
    lines.append(
        f"- Adapter test double: {double.get('status')} "
        f"({double.get('label', 'not an LLM synthetic user')})."
    )
    lines.extend(["", "## Versions", ""])
    for key, value in report["versions"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append(report["note"])
    lines.append("")
    return "\n".join(lines)
