#!/usr/bin/env python3
"""Playwright screenshots and axe-core for the haunted page.

Starts the local server, writes gallery/*.png and gallery/axe-report.json,
and exits non-zero when axe reports a violation or an incomplete result.
Does not deploy. Reduced motion is on so ghost text stays visible.
"""

from __future__ import annotations

import json
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demos" / "haunted"))
sys.path.insert(0, str(ROOT / "src"))

from server import make_server  # noqa: E402

GALLERY = ROOT / "gallery"
AXE = ROOT / "validation" / "node_modules" / "axe-core" / "axe.min.js"

SHOTS = [
    ("01-hero", "/", "#hero", False),
    ("02-judge-letter", "/?judge=1", "#artifact", True),
    ("03-cited-responsibility", "/", "#verdict", False),
    ("04-not-found", "/", "#verdict", False),
    ("05-mixed", "/", "#claims", False),
    ("06-lease-cited", "/", "#verdict", False),
    ("07-lease-file", "/", "#artifact", False),
    ("08-paste-postcard", "/", "#claims", False),
]


def _axe(page) -> dict:
    page.add_script_tag(path=str(AXE))
    result = page.evaluate(
        """() => axe.run({ resultTypes: ['violations', 'incomplete'] })"""
    )
    return {
        "violations": len(result["violations"]),
        "incomplete": len(result["incomplete"]),
        "violation_ids": [item["id"] for item in result["violations"]],
        "incomplete_ids": [item["id"] for item in result["incomplete"]],
        "nodes": [
            {
                "id": item["id"],
                "impact": item.get("impact"),
                "targets": [node["target"] for node in item.get("nodes", [])],
            }
            for item in result["violations"] + result["incomplete"]
        ],
    }


def main() -> int:
    if not AXE.is_file():
        print(f"missing {AXE}", file=sys.stderr)
        return 2
    from playwright.sync_api import sync_playwright

    GALLERY.mkdir(parents=True, exist_ok=True)
    httpd = make_server(0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address
    base = f"http://{host}:{port}"
    pages = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                reduced_motion="reduce",
            )
            page = context.new_page()
            page.set_default_timeout(10000)
            errors: list[str] = []
            page.on("pageerror", lambda exc: errors.append(str(exc)[:300]))

            def shoot(name: str, full: bool) -> None:
                page.screenshot(path=str(GALLERY / f"{name}.png"), full_page=full)
                report = _axe(page)
                report["id"] = name
                report["url"] = page.url
                pages.append(report)
                print(f"{name} violations={report['violations']} incomplete={report['incomplete']}")

            page.goto(base + "/", wait_until="domcontentloaded")
            page.wait_for_selector("#hero")
            page.wait_for_function("() => document.querySelector('#source').textContent.includes('$42.15')")
            shoot("01-hero", False)

            page.goto(base + "/?judge=1", wait_until="domcontentloaded")
            page.wait_for_function(
                "() => document.querySelector('#artifact').textContent.includes('Status: cited')"
            )
            page.wait_for_function(
                "() => document.querySelector('#verdict').textContent.length > 0"
            )
            shoot("02-judge-letter", True)

            page.goto(base + "/", wait_until="domcontentloaded")
            page.wait_for_selector("#source")
            page.get_by_role("button", name="Patient responsibility").click()
            page.wait_for_function("() => document.querySelector('#verdict').textContent.includes('Cited')")
            shoot("03-cited-responsibility", False)

            page.get_by_role("button", name="Missing penalty").click()
            page.wait_for_function("() => document.querySelector('#verdict').textContent.includes('Ghost')")
            shoot("04-not-found", False)

            page.get_by_role("button", name="Cited and ghost").click()
            page.wait_for_function("() => document.querySelector('#claims').children.length === 2")
            shoot("05-mixed", False)

            page.get_by_role("radio", name="Sample lease").check()
            page.wait_for_function("() => document.querySelector('#source').textContent.includes('security deposit')")
            page.get_by_role("button", name="Security deposit").click()
            page.wait_for_function("() => document.querySelector('#verdict').textContent.includes('Cited')")
            shoot("06-lease-cited", False)

            page.get_by_role("button", name="Build the workflow file").click()
            page.wait_for_function(
                "() => document.querySelector('#artifact').textContent.includes('Synthetic clause issues')"
            )
            shoot("07-lease-file", True)

            page.get_by_role("radio", name="Paste a document").check()
            page.get_by_role("button", name="Postcard").click()
            page.wait_for_function("() => document.querySelector('#claims').children.length === 2")
            shoot("08-paste-postcard", False)

            browser.close()
        if errors:
            print("page errors:", errors, file=sys.stderr)
            return 1
    finally:
        httpd.shutdown()
        httpd.server_close()

    violations = sum(item["violations"] for item in pages)
    payload = {"tool": "axe-core", "violations": violations, "pages": pages}
    (GALLERY / "axe-report.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"violations {violations} across {len(pages)} pages")
    return 1 if violations or any(item["incomplete"] for item in pages) else 0


if __name__ == "__main__":
    sys.exit(main())
