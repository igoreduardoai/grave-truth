"""Run a list of deterministic browser actions. Not a persona."""

from __future__ import annotations

from validation.checks import mark_support, marks_are_document_slices


class CheckError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


def run_actions(page, actions: list[dict]) -> dict:
    checks: list[dict] = []
    limitations: list[dict] = []
    pasted = ""
    failure = ""
    for action in actions:
        label = _label(action)
        try:
            outcome = _apply(page, action, pasted)
        except CheckError as exc:
            checks.append({"name": label, "passed": False, "detail": exc.detail})
            failure = exc.detail
            break
        except Exception as exc:
            detail = str(exc).split("\n", 1)[0][:400]
            checks.append({"name": label, "passed": False, "detail": detail})
            failure = detail
            break
        if action.get("do") == "fill" and action.get("label") == "Pasted document":
            pasted = action.get("text") or ""
        if outcome and outcome.get("limitation"):
            limitations.append(outcome["limitation"])
        checks.append({"name": label, "passed": True, "detail": (outcome or {}).get("detail", "")})
    passed = sum(1 for check in checks if check["passed"])
    return {
        "checks": checks,
        "checks_passed": passed,
        "checks_total": len(actions),
        "completed": bool(actions) and passed == len(actions) and not failure,
        "failure_detail": failure,
        "limitations": limitations,
        "observed_marks": _marks(page),
    }


def _apply(page, action: dict, pasted: str) -> dict | None:
    kind = action.get("do")
    if kind == "check":
        page.get_by_role(action["role"], name=action["name"]).check()
        return None
    if kind == "click":
        page.get_by_role(action["role"], name=action["name"]).click()
        return None
    if kind == "fill":
        page.get_by_label(action["label"]).fill(action.get("text") or "")
        return None
    if kind == "press":
        page.keyboard.press(action["key"])
        return None
    if kind == "focus":
        page.get_by_label(action["label"]).focus()
        return None
    if kind == "expect_focused":
        focused = page.evaluate(
            """(selector) => {
              const el = document.querySelector(selector);
              return !!el && el === document.activeElement;
            }""",
            action["selector"],
        )
        if not focused:
            active = page.evaluate(
                """() => {
                  const el = document.activeElement;
                  if (!el) return "none";
                  return el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") + "." + (el.className || "");
                }"""
            )
            raise CheckError(f"focus was {active}, expected {action['selector']}")
        return None
    if kind == "expect_text":
        locator = page.locator(action["selector"])
        locator.wait_for(state="visible", timeout=8000)
        text = locator.inner_text(timeout=8000)
        if action["includes"] not in text:
            raise CheckError(f"{action['selector']} was {text!r}")
        return None
    if kind == "expect_class":
        page.wait_for_function(
            """([selector, name]) => {
              const el = document.querySelector(selector);
              if (!el || !el.className) return false;
              return el.className.split(/\\s+/).includes(name);
            }""",
            arg=[action["selector"], action["class_name"]],
            timeout=8000,
        )
        return None
    if kind == "expect_visible":
        page.locator(action["selector"]).wait_for(state="visible", timeout=8000)
        return None
    if kind == "expect_marks":
        page.locator("mark.clause").first.wait_for(state="visible", timeout=8000)
        result = mark_support(_marks(page), require=action.get("require") or [], forbid=action.get("forbid") or [])
        if not result["ok"]:
            raise CheckError(
                f"marks {result['marks']!r}; missing {result['missing']}; forbidden {result['forbidden_hits']}"
            )
        return None
    if kind == "expect_no_marks":
        count = page.locator("mark.clause").count()
        if count:
            raise CheckError(f"expected no marks, found {count}")
        return None
    if kind == "expect_claim_ghost":
        claim = page.locator(".claim.is-ghost").filter(has_text=action["text"])
        if claim.count() < 1:
            raise CheckError(f"no ghost claim containing {action['text']!r}")
        return None
    if kind == "expect_marks_in_pasted":
        result = marks_are_document_slices(_marks(page), pasted)
        if not result["ok"]:
            raise CheckError(f"marks were not slices of the pasted document: {result}")
        return None
    if kind == "limitation_if_mark_includes":
        marks = _marks(page)
        joined = "\n".join(marks)
        if action["text"] in joined:
            return {
                "limitation": {
                    "id": action.get("id") or "mark-observation",
                    "detail": action["detail"],
                    "observed_marks": marks,
                }
            }
        return {"detail": "condition not observed"}
    raise CheckError(f"unknown action {kind}")


def _marks(page) -> list[str]:
    return [text.strip() for text in page.locator("mark.clause").all_text_contents()]


def _label(action: dict) -> str:
    kind = action.get("do", "action")
    hint = action.get("name") or action.get("label") or action.get("selector") or action.get("includes") or ""
    return f"{kind} {hint}".strip()
