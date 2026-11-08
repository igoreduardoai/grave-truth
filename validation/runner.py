"""One local run. No model call unless the app config and the environment both opt in."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from validation.browser_run import run_browser_layers
from validation.config import PACKAGE, load_app
from validation.gold import run_gold
from validation.persona import llm_persona_status
from validation.holdout_eval import measure as measure_holdout
from validation.readiness import decide
from validation.report import build_report, summarize_profiles, write_report
from validation.servers import start_product_server, stop_process

ROOT = PACKAGE.parent


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    app_id = "grave-truth"
    if args and args[0] == "check-config":
        load_app(app_id if len(args) == 1 else args[1])
        print(f"config ok: {app_id if len(args) == 1 else args[1]}")
        return 0
    if args and args[0] == "run":
        args = args[1:]
    if args and args[0] == "--app":
        app_id = args[1]
    config = load_app(app_id)
    report, ok = execute(config)
    published = ROOT / "validation" / "reports"
    write_report(report, published)
    stamp = report["date"].replace(":", "").replace("+00:00", "Z")
    write_report(report, published / "runs" / stamp)
    print(f"wrote {published / 'OBSERVED.md'}")
    counts = summarize_profiles(report["scripted_profiles"]["tasks"])
    print(
        "scripted {tasks_completed}/{tasks_attempted}; "
        "citation {citation_correct}/{citation_applicable}; "
        "refusal {refusal_correct}/{refusal_applicable}".format(**counts)
    )
    print(f"llm persona: {report['persona']['llm']['status']}")
    return 0 if ok else 1


def execute(config: dict) -> tuple[dict, bool]:
    commit = _commit()
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    gold = run_gold(ROOT)
    llm = llm_persona_status(config, dict(os.environ))
    run_dir = ROOT / "validation" / "reports" / "runs" / "current"
    if run_dir.exists():
        import shutil
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    proc = None
    browser = None
    try:
        proc, base_url = start_product_server(ROOT, "demos/haunted/server.py")
        browser = run_browser_layers(ROOT, config, base_url, run_dir)
        lighthouse = run_lighthouse(base_url, browser["chrome"], run_dir / "lighthouse.json")
    finally:
        stop_process(proc)
    versions = _versions(browser["chrome"] if browser else None)
    axe = browser["axe"]
    double = browser["double"]
    probe = browser["probe"]
    negative = browser["negative"]
    profiles = _relativize(browser["profiles"], ROOT)
    holdout = measure_holdout(ROOT)
    journeys_ok = all(item["completed"] for item in profiles)
    stability = browser.get("stability") or {}
    if stability.get("status") == "exercised" and not stability.get("stable"):
        journeys_ok = False
    negatives_ok = bool(negative) and all(item["caught"] for item in negative)
    guards_ok = bool(probe.get("caught"))
    layers = {
        "pytest_and_gold": {**gold, "status": "exercised" if gold["ok"] else "failed", "ok": gold["ok"]},
        "scripted_browser": {
            "status": "exercised" if journeys_ok else "failed",
            "tool": "playwright",
            "ok": journeys_ok,
            "note": "Deterministic scripted profiles. Not LLM synthetic users.",
        },
        "negative_controls": {
            "status": "exercised" if negatives_ok else "failed",
            "ok": negatives_ok,
            "exercised": True,
        },
        "browser_guards": {
            "status": "exercised" if guards_ok else "failed",
            "ok": guards_ok,
            "exercised": True,
        },
        "axe_core": {
            "status": axe["status"],
            "exercised": axe.get("exercised", False),
            "ok": bool(axe.get("exercised")),
            "violation_count": axe.get("violation_count"),
            "incomplete_count": axe.get("incomplete_count"),
            "states": axe.get("states") or [],
            "note": axe.get("note") or axe.get("reason"),
        },
        "lighthouse": lighthouse,
        "holdout": {
            "status": "exercised",
            "exercised": True,
            "ok": True,
            "intended_met": holdout["intended_met"],
            "attempted": holdout["attempted"],
            "note": "Measurement of held-out cases. A miss is disclosed, not tuned away in this run.",
        },
        "stability": stability,
        "persona_llm": llm,
    }
    contrast = None
    for state in axe.get("states") or []:
        if state.get("contrast"):
            contrast = state["contrast"]
    unresolved = []
    if holdout["intended_met"] != holdout["attempted"]:
        misses = [row["id"] for row in holdout["cases"] if not row["intended_met"]]
        unresolved.append(
            f"holdout intended {holdout['intended_met']}/{holdout['attempted']}: {', '.join(misses)}"
        )
    if axe.get("incomplete_count"):
        ratio = (contrast or {}).get("ratio_versus_declared_background")
        unresolved.append(
            "axe color-contrast incomplete remains"
            + (f"; eyebrow versus #120e16 measured {ratio}:1" if ratio is not None else "")
            + "; the rule was not disabled"
        )
    if config.get("submission", {}).get("rules_check") != "automatically_verified":
        unresolved.append("sponsor and new-work rules were not automatically verified")
    persona = {
        "runner": "ux-swarm-adapted",
        "upstream": "https://github.com/masonomara/ux-swarm/commit/71197bc9d4800a9ecac863e7b5eee1f121e287a5",
        "llm": llm,
        "adapter_test_double": _relativize_tree(double, ROOT),
        "safety_probe": _relativize_tree(probe, ROOT),
    }
    findings = []
    for state in axe.get("states") or []:
        for item in state.get("violations") or []:
            findings.append({"state": state["state"], "tool": "axe-core", **item})
    decision = decide(config, {"layers": layers, "holdout": holdout, "unresolved": unresolved})
    report = build_report({
        "app_id": config["id"],
        "repo": _repo(),
        "commit": commit,
        "date": date,
        "model_api_calls": llm.get("calls", 0),
        "versions": versions,
        "layers": layers,
        "holdout": holdout,
        "decision": decision,
        "scripted_profiles": profiles,
        "negative_controls": negative,
        "axe_findings": findings,
        "limitations": browser["limitations"],
        "ux_hypotheses": [],
        "persona": persona,
    })
    report["cost_usd_observed"] = float(llm.get("cost_usd_observed") or 0) + float(double.get("cost_usd_observed") or 0)
    report["contrast"] = contrast
    ok = _ok(gold, profiles, negative, double, probe, axe, lighthouse, stability)
    report["automated_commands_ok"] = ok
    return report, ok


def _ok(gold, profiles, negative, double, probe, axe, lighthouse, stability) -> bool:
    stable = stability.get("status") != "exercised" or stability.get("stable") is True
    return bool(
        gold["ok"]
        and profiles
        and all(item["completed"] for item in profiles)
        and negative
        and all(item["caught"] for item in negative)
        and double.get("ok")
        and probe.get("caught")
        and axe.get("exercised")
        and lighthouse.get("status") == "diagnostic"
        and stable
    )


def _repo() -> str:
    completed = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    url = completed.stdout.strip()
    if "@" in url:
        url = "https://" + url.split("@", 1)[1]
    return url.removesuffix(".git")


def run_lighthouse(url: str, chrome: str | None, out_path: Path) -> dict:
    cli = ROOT / "validation" / "node_modules" / "lighthouse" / "cli" / "index.js"
    if not cli.exists():
        return {"status": "skipped", "exercised": False, "reason": "lighthouse is not installed"}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    if chrome:
        env["CHROME_PATH"] = chrome
    command = [
        "node",
        str(cli),
        url,
        "--quiet",
        "--chrome-flags=--headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage",
        "--output=json",
        f"--output-path={out_path}",
        "--only-categories=performance,best-practices",
        "--max-wait-for-load=20000",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "skipped", "exercised": False, "reason": "lighthouse timed out"}
    if completed.returncode != 0 or not out_path.exists():
        tail = (completed.stderr or completed.stdout or "")[-800:]
        return {"status": "skipped", "exercised": False, "reason": tail or f"exit {completed.returncode}"}
    data = json.loads(out_path.read_text(encoding="utf-8"))
    audits = data.get("audits") or {}
    settings = data.get("configSettings") or {}
    categories = {}
    for name, category in (data.get("categories") or {}).items():
        categories[name] = {"title": category.get("title"), "lab_score": category.get("score")}
    return {
        "status": "diagnostic",
        "exercised": True,
        "lighthouse_version": data.get("lighthouseVersion"),
        "requested_url": data.get("requestedUrl"),
        "fetch_time": data.get("fetchTime"),
        "form_factor": settings.get("formFactor"),
        "throttling_method": settings.get("throttlingMethod"),
        "screen_emulation_mobile": (settings.get("screenEmulation") or {}).get("mobile"),
        "lab_category_scores": categories,
        "metrics": {
            key: (audits.get(key) or {}).get("numericValue")
            for key in (
                "first-contentful-paint",
                "largest-contentful-paint",
                "total-blocking-time",
                "cumulative-layout-shift",
                "speed-index",
            )
        },
        "note": (
            "Laboratory figures from this machine. Not a field measurement, "
            "not a harness pass/fail gate, and not a quality score for the product."
        ),
    }


def _versions(chrome: str | None) -> dict:
    import importlib.metadata

    def package_version(name: str) -> str:
        path = ROOT / "validation" / "node_modules" / name / "package.json"
        if not path.exists():
            return "not installed"
        return json.loads(path.read_text(encoding="utf-8")).get("version", "unknown")

    try:
        playwright_version = importlib.metadata.version("playwright")
    except importlib.metadata.PackageNotFoundError:
        playwright_version = "not installed"
    return {
        "python": sys.version.split()[0],
        "playwright": playwright_version,
        "axe_core": package_version("axe-core"),
        "lighthouse": package_version("lighthouse"),
        "chromium_executable": chrome or "not launched",
        "ux_swarm_adapted_from": "71197bc9d4800a9ecac863e7b5eee1f121e287a5",
        "ghostuser_evaluated_not_used": "17eaef154011ef93351a127da31cd7216bdd8c8c",
    }


def _commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.stdout.strip() or "unknown"


def _relativize(profiles: list[dict], root: Path) -> list[dict]:
    return [_relativize_tree(profile, root) for profile in profiles]


def _relativize_tree(value, root: Path):
    if isinstance(value, dict):
        return {key: _relativize_tree(item, root) for key, item in value.items()}
    if isinstance(value, list):
        return [_relativize_tree(item, root) for item in value]
    if isinstance(value, str) and value.startswith("/"):
        path = Path(value)
        try:
            return str(path.resolve().relative_to(root))
        except ValueError:
            return value
    return value
