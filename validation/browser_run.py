"""Playwright session: scripted profiles, axe-core, and the persona loop."""

from __future__ import annotations

import shutil
from pathlib import Path

from validation.allowlist import navigation_allowed
from validation.executor import run_actions
from validation.persona import ReplayDecider, run_browser_steps
from validation.report import negative_control_caught

AXE_RUN = """() => axe.run({
  resultTypes: ['violations', 'incomplete']
})"""


def run_browser_layers(root: Path, config: dict, base_url: str, fixture_html: bytes, run_dir: Path) -> dict:
    from playwright.sync_api import sync_playwright

    evidence = root / "validation" / "reports" / "evidence"
    if evidence.exists():
        shutil.rmtree(evidence)
    evidence.mkdir(parents=True)
    traces = run_dir / "traces"
    traces.mkdir(parents=True, exist_ok=True)
    axe_path = root / "validation" / "node_modules" / "axe-core" / "axe.min.js"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        chrome = playwright.chromium.executable_path
        profiles = [
            _profile(browser, base_url, profile, evidence, traces)
            for profile in config["scripted_profiles"]
        ]
        limitations = [item for profile in profiles for item in profile.pop("limitations", [])]
        axe = _axe(browser, base_url, axe_path, evidence, traces)
        double = _double(browser, base_url, config["persona_double"], evidence / "adapter-test-double", traces)
        probe, negative = _fixture_layers(browser, config, fixture_html, evidence, traces)
        browser.close()

    return {
        "profiles": profiles,
        "limitations": limitations,
        "axe": axe,
        "double": double,
        "probe": probe,
        "negative": negative,
        "chrome": chrome,
    }


def _context(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        ignore_https_errors=False,
    )
    context.route("**/*", _route)
    context.tracing.start(screenshots=True, snapshots=True, sources=False)
    return context


def _route(route) -> None:
    url = route.request.url
    if url.startswith("data:") or url.startswith("blob:"):
        route.continue_()
        return
    if not navigation_allowed(url):
        route.abort()
        return
    route.continue_()


def _profile(browser, base_url: str, profile: dict, evidence: Path, traces: Path) -> dict:
    context = _context(browser)
    page = context.new_page()
    page.set_default_timeout(8000)
    console_errors: list[str] = []
    page.on("console", lambda msg: _console(msg, console_errors))
    page.on("pageerror", lambda exc: console_errors.append(str(exc)[:300]))
    page.goto(base_url, wait_until="domcontentloaded")
    outcome = run_actions(page, profile["actions"])
    shot = evidence / f"{profile['id']}.png"
    page.screenshot(path=str(shot))
    context.tracing.stop(path=str(traces / f"{profile['id']}.zip"))
    context.close()
    if console_errors and outcome["completed"]:
        outcome["completed"] = False
        outcome["failure_detail"] = "console error: " + console_errors[0]
    failure = outcome["failure_detail"]
    return {
        "id": profile["id"],
        "kind": "scripted_profile",
        "category": profile.get("category", "journey"),
        "citation": bool(profile.get("citation")),
        "refusal": bool(profile.get("refusal")),
        "completed": outcome["completed"],
        "checks_passed": outcome["checks_passed"],
        "checks_total": outcome["checks_total"],
        "checks": outcome["checks"],
        "failure_detail": failure,
        "observed_marks": outcome["observed_marks"],
        "limitations": outcome["limitations"],
        "console_errors": console_errors,
        "screenshot": str(shot.relative_to(evidence.parents[1])) if False else str(shot),
        "llm_synthetic_user": False,
    }


def _console(msg, bucket: list[str]) -> None:
    if msg.type != "error":
        return
    text = msg.text
    if "favicon" in text.lower() or "status of 400" in text:
        return
    bucket.append(text[:300])


def _axe(browser, base_url: str, axe_path: Path, evidence: Path, traces: Path) -> dict:
    if not axe_path.exists():
        return {"status": "skipped", "exercised": False, "reason": f"missing {axe_path.name}", "states": []}
    states = []
    states.append(_axe_state(browser, base_url, axe_path, evidence, traces, "initial", prepare=None))
    states.append(_axe_state(browser, base_url, axe_path, evidence, traces, "cited-eob", prepare=_cite_eob))
    violations = [item for state in states for item in state["violations"]]
    return {
        "status": "exercised",
        "exercised": True,
        "engine": "axe-core",
        "states": states,
        "violation_count": len(violations),
        "incomplete_count": sum(state["incomplete_count"] for state in states),
        "note": "Rule findings are not a conformance certificate and are not a harness grade.",
    }


def _cite_eob(page) -> None:
    page.get_by_label("Question").fill("What is the patient responsibility?")
    page.get_by_label("Proposed answer").fill("")
    page.get_by_role("button", name="Check grounding").click()
    page.locator("mark.clause").first.wait_for(state="visible", timeout=8000)


def _axe_state(browser, base_url, axe_path: Path, evidence: Path, traces: Path, name: str, prepare) -> dict:
    context = _context(browser)
    page = context.new_page()
    try:
        page.goto(base_url, wait_until="domcontentloaded")
        if prepare:
            prepare(page)
        page.screenshot(path=str(evidence / f"axe-{name}.png"))
        page.add_script_tag(path=str(axe_path))
        raw = page.evaluate(AXE_RUN)
    finally:
        context.tracing.stop(path=str(traces / f"axe-{name}.zip"))
        context.close()
    violations = [_compact(item) for item in raw.get("violations") or []]
    incomplete = [_compact(item) for item in raw.get("incomplete") or []]
    return {
        "state": name,
        "violation_count": len(violations),
        "incomplete_count": len(incomplete),
        "violations": violations,
        "incomplete": incomplete,
    }


def _compact(item: dict) -> dict:
    nodes = item.get("nodes") or []
    sample = ""
    if nodes:
        sample = (nodes[0].get("html") or "")[:180]
    return {
        "id": item.get("id"),
        "impact": item.get("impact"),
        "help": item.get("help"),
        "node_count": len(nodes),
        "sample": sample,
    }


def _double(browser, base_url: str, spec: dict, evidence: Path, traces: Path) -> dict:
    context = _context(browser)
    page = context.new_page()
    page.set_default_timeout(8000)
    page.goto(base_url, wait_until="domcontentloaded")
    result = run_browser_steps(
        page,
        ReplayDecider(spec["steps"]),
        max_steps=int(spec.get("max_steps") or 6),
        evidence_dir=evidence,
        label="adapter test double, not an LLM synthetic user",
    )
    context.tracing.stop(path=str(traces / "adapter-test-double.zip"))
    context.close()
    result["ok"] = result["status"] == "script_finished" and not result["blockers"]
    result["status"] = "exercised" if result["ok"] else "failed"
    return result


def _fixture_layers(browser, config: dict, html: bytes, evidence: Path, traces: Path) -> tuple[dict, list[dict]]:
    from validation.servers import FixtureServer

    server = FixtureServer(html)
    url = server.start()
    try:
        probe = _probe(browser, url, config["safety_probe"], evidence / "safety-probe", traces)
        negative = []
        for control in config["negative_controls"]:
            negative.append(_negative(browser, url, control, evidence, traces))
    finally:
        server.stop()
    return probe, negative


def _probe(browser, url: str, spec: dict, evidence: Path, traces: Path) -> dict:
    context = _context(browser)
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")
    result = run_browser_steps(
        page,
        ReplayDecider(spec["steps"]),
        max_steps=int(spec.get("max_steps") or 4),
        evidence_dir=evidence,
        label="safety probe, not an LLM synthetic user",
    )
    context.tracing.stop(path=str(traces / "safety-probe.zip"))
    context.close()
    blocked = any(item["category"] == "off_allowlist" for item in result["blockers"])
    local = result["final_host"] in {"127.0.0.1", "localhost"}
    leaked = any(host == "example.com" for host in result["response_hosts"])
    result["caught"] = blocked and local and not leaked
    result["ok"] = result["caught"]
    result["status"] = "caught" if result["caught"] else "missed"
    result["kind"] = "safety_probe"
    result["llm_synthetic_user"] = False
    return result


def _negative(browser, url: str, control: dict, evidence: Path, traces: Path) -> dict:
    context = _context(browser)
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")
    outcome = run_actions(page, control["actions"])
    page.screenshot(path=str(evidence / f"{control['id']}.png"))
    context.tracing.stop(path=str(traces / f"{control['id']}.zip"))
    context.close()
    caught = negative_control_caught(outcome["checks"])
    return {
        "id": control["id"],
        "kind": "negative_control",
        "caught": caught,
        "planted_failure_detected": caught,
        "checks": outcome["checks"],
        "llm_synthetic_user": False,
    }
