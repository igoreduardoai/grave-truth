"""Full axe run (all rules) on the redesigned page at 1280x800 and 390x844, default and judge mode."""

from pathlib import Path

from playwright.sync_api import sync_playwright

from validation.servers import start_product_server, stop_process

ROOT = Path(__file__).resolve().parents[1]
AXE = ROOT / "validation" / "node_modules" / "axe-core" / "axe.min.js"


def test_axe_has_no_violations_at_desktop_and_phone_widths():
    assert AXE.is_file(), "axe-core is required and must stay enabled"
    proc, url = start_product_server(ROOT, "demos/haunted/server.py")
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
            try:
                for width, height in ((1280, 800), (390, 844)):
                    for suffix in ("", "?judge=1"):
                        page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce")
                        page.goto(url + suffix, wait_until="networkidle")
                        page.locator("mark.clause").first.wait_for(state="visible", timeout=8000)
                        page.add_script_tag(path=str(AXE))
                        raw = page.evaluate("() => axe.run(document)")
                        found = [f"{v['id']}: {v['nodes'][0]['html'][:80]}" for v in raw.get("violations") or []]
                        assert not found, f"{width}{suffix}: {found}"
                        overflow = page.evaluate(
                            "() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"
                        )
                        assert overflow, f"{width}{suffix}: horizontal overflow"
                        page.close()
            finally:
                browser.close()
    finally:
        stop_process(proc)
