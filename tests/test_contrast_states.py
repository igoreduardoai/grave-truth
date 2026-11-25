"""The two haunted-demo states axe checks must have a resolved, passing contrast.

This fails while the body background is a gradient: axe-core reports
color-contrast incomplete because it cannot decide the background color.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

from validation.contrast import assess_rendered_text
from validation.servers import start_product_server, stop_process

ROOT = Path(__file__).resolve().parents[1]
AXE = ROOT / "validation" / "node_modules" / "axe-core" / "axe.min.js"
COLLECT = """() => {
  const nodes = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const text = walker.currentNode.textContent.replace(/\\s+/g, ' ').trim();
    if (!text) continue;
    const el = walker.currentNode.parentElement;
    if (!el) continue;
    const style = getComputedStyle(el);
    if (style.display === 'none' || style.visibility === 'hidden') continue;
    const layers = [];
    let current = el;
    while (current) {
      const computed = getComputedStyle(current);
      layers.push({
        backgroundColor: computed.backgroundColor,
        backgroundImage: computed.backgroundImage,
        opacity: computed.opacity,
      });
      current = current.parentElement;
    }
    nodes.push({
      text: text.slice(0, 80),
      color: style.color,
      fontSize: style.fontSize,
      fontWeight: style.fontWeight,
      opacity: style.opacity,
      layers,
    });
  }
  return nodes;
}"""


def _cite_eob(page) -> None:
    page.get_by_label("Question").fill("What is the patient responsibility?")
    page.get_by_label("Proposed answer").fill("")
    page.get_by_role("button", name="Check grounding").click()
    page.locator("mark.clause").first.wait_for(state="visible", timeout=8000)


def _contrast_messages(raw: dict) -> list[str]:
    messages = []
    for item in raw.get("incomplete") or []:
        if item.get("id") != "color-contrast":
            continue
        for node in item.get("nodes") or []:
            for bucket in ("any", "all", "none"):
                for check in node.get(bucket) or []:
                    message = check.get("message")
                    if message and message not in messages:
                        messages.append(message)
    for item in raw.get("violations") or []:
        if item.get("id") == "color-contrast":
            messages.append(item.get("help") or "color-contrast violation")
    return messages


def test_axe_contrast_states_are_resolvable_and_passing():
    assert AXE.is_file(), "axe-core is required and must stay enabled"
    proc, url = start_product_server(ROOT, "demos/haunted/server.py")
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
            try:
                for name, prepare in (("initial", None), ("cited-eob", _cite_eob)):
                    page = browser.new_page(viewport={"width": 1280, "height": 800})
                    page.goto(url, wait_until="domcontentloaded")
                    if prepare:
                        prepare(page)
                    page.add_script_tag(path=str(AXE))
                    raw = page.evaluate(
                        "() => axe.run({ resultTypes: ['violations', 'incomplete'] })"
                    )
                    incomplete = [
                        item for item in (raw.get("incomplete") or []) if item.get("id") == "color-contrast"
                    ]
                    violations = [
                        item for item in (raw.get("violations") or []) if item.get("id") == "color-contrast"
                    ]
                    rendered = [
                        assess_rendered_text(
                            color=node["color"],
                            font_size=node["fontSize"],
                            font_weight=node["fontWeight"],
                            opacity=node["opacity"],
                            layers=node["layers"],
                        )
                        | {"text": node["text"]}
                        for node in page.evaluate(COLLECT)
                    ]
                    unresolved = [item for item in rendered if not item["resolvable"]]
                    failing = [item for item in rendered if item["resolvable"] and not item["passes"]]
                    assert not incomplete and not violations, (
                        f"{name}: axe color-contrast is not a resolved pass "
                        f"(incomplete {len(incomplete)}, violations {len(violations)}): "
                        f"{_contrast_messages(raw)}"
                    )
                    assert not unresolved, (
                        f"{name}: rendered background is not a solid color: "
                        f"{[(item['text'], item['reason']) for item in unresolved[:4]]}"
                    )
                    assert not failing, (
                        f"{name}: rendered contrast is below AA: "
                        f"{[(item['text'], item['ratio'], item['required']) for item in failing[:4]]}"
                    )
                    assert rendered, f"{name}: no text nodes were measured"
            finally:
                browser.close()
    finally:
        stop_process(proc)
