#!/usr/bin/env python3
"""Record a silent Playwright walkthrough of the local demo.

The walk opens the hero, ?judge=1 and the export letter, /health, and the
capability matrix page. Synthetic fixtures only. No microphone and no
synthesized speech.

Caption numbers have to appear in output this process runs or reads:
evals/run_gold_and_holdout.py, the contrast count below, gallery/axe-report.json,
and demo/pytest-last.txt. Any other number stops the script.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "demos" / "haunted"))

from server import make_server  # noqa: E402

from grave_truth.apps import eob, lease  # noqa: E402
from grave_truth.artifact import build_artifact  # noqa: E402

DEMO = ROOT / "demo"
AXE = ROOT / "validation" / "node_modules" / "axe-core" / "axe.min.js"
PYTEST_LOG = DEMO / "pytest-last.txt"
MEASUREMENTS = DEMO / "measurements.txt"
TIMING = DEMO / "timing.txt"
VIDEO = DEMO / "raw-walkthrough.webm"
CAPTIONS = DEMO / "captions.srt"
SHOTLIST = DEMO / "SHOTLIST.md"
GITIGNORE = ROOT / ".gitignore"
VIDEO_LIMIT = 10 * 1024 * 1024
GITIGNORE_BLOCK = (
    "# Raw demo recording. Present only while the file is larger than 10MB.\n"
    "demo/raw-walkthrough.webm\n"
)
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


def measure_contrast() -> dict[str, int]:
    """Same counts as tests/test_capability_contrast.py, printed for captions."""
    cases = json.loads((ROOT / "evals" / "gold_cases.json").read_text(encoding="utf-8"))
    missing = [case for case in cases if case["expect"] == "not_found"]
    cited_by_checker = 0
    cited_by_first_sentence = 0
    for case in missing:
        agent = eob.load_agent() if case["app"] == "eob" else lease.load_agent()
        if agent.answer(case["question"]).citations:
            cited_by_checker += 1
        fixture = eob.FIXTURE if case["app"] == "eob" else lease.FIXTURE
        if fixture.read_text(encoding="utf-8").splitlines()[0]:
            cited_by_first_sentence += 1
    linked = 0
    for app in ("eob", "lease"):
        artifact = build_artifact(app)
        linked += sum(len(item["citations"]) for item in artifact["items"])
    return {
        "cases": len(missing),
        "checker": cited_by_checker,
        "first_sentence": cited_by_first_sentence,
        "export_spans": linked,
        "copy_spans": 0,
    }


def number_in_source(number: str, source: str) -> bool:
    return re.search(rf"(?<!\d){re.escape(number)}(?!\d)", source) is not None


def assert_caption_numbers(text: str, source: str) -> None:
    missing = [number for number in NUMBER_RE.findall(text) if not number_in_source(number, source)]
    if missing:
        raise SystemExit(
            "caption number not in measurement output: " + ", ".join(missing)
        )


def _must_line(text: str, pattern: str, label: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise SystemExit(f"missing {label} in measurement output")
    return match.group(0)


def collect_measurements() -> str:
    if not PYTEST_LOG.is_file():
        raise SystemExit(f"missing {PYTEST_LOG}. Run pytest and save its output there first.")
    if not (ROOT / "gallery" / "axe-report.json").is_file():
        raise SystemExit("missing gallery/axe-report.json. Run scripts/capture_gallery.py first.")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "evals" / "run_gold_and_holdout.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stdout + proc.stderr)
    pytest_text = PYTEST_LOG.read_text(encoding="utf-8")
    pytest_line = _must_line(pytest_text, r"^\d+ passed.*$", "pytest summary")
    eval_passed = _must_line(proc.stdout, r"^\d+/\d+ passed$", "eval total")
    eval_summary = _must_line(
        proc.stdout,
        r"^accept_grounded \d+, cited \d+, not_found \d+, reject_ungrounded \d+$",
        "eval summary",
    )
    holdout = _must_line(proc.stdout, r"^holdout \d+/\d+$", "holdout line")
    contrast = measure_contrast()
    report = json.loads((ROOT / "gallery" / "axe-report.json").read_text(encoding="utf-8"))
    incomplete = sum(page["incomplete"] for page in report["pages"])
    lines = [
        eval_passed,
        eval_summary,
        holdout,
        f"contrast checker cited {contrast['checker']} of {contrast['cases']}",
        f"contrast first sentence cited {contrast['first_sentence']} of {contrast['cases']}",
        f"contrast export spans {contrast['export_spans']}",
        f"contrast copy spans {contrast['copy_spans']}",
        f"axe violations {report['violations']}",
        f"axe pages {len(report['pages'])}",
        f"axe incomplete {incomplete}",
        pytest_line,
    ]
    return "\n".join(lines) + "\n"


def caption_texts(source: str) -> list[str]:
    """Sentences whose digits are copied from measurement lines."""
    texts = [
        "Synthetic fixtures only. No voice. The hero shows input, check, and result.",
        _must_line(source, r"^\d+/\d+ passed$", "eval total")
        + ". "
        + _must_line(
            source,
            r"^accept_grounded \d+, cited \d+, not_found \d+, reject_ungrounded \d+$",
            "eval summary",
        )
        + ".",
        _must_line(source, r"^contrast checker cited \d+ of \d+$", "contrast checker")
        + ". "
        + _must_line(source, r"^contrast first sentence cited \d+ of \d+$", "contrast baseline")
        + ". "
        + _must_line(source, r"^contrast export spans \d+$", "export spans")
        + ". "
        + _must_line(source, r"^contrast copy spans \d+$", "copy spans")
        + ".",
        "GET /health is static JSON. The live model path is unimplemented. "
        + _must_line(source, r"^holdout \d+/\d+$", "holdout")
        + ".",
        "Capability matrix from the repository file. "
        + _must_line(source, r"^axe violations \d+$", "axe violations")
        + ". "
        + _must_line(source, r"^axe incomplete \d+$", "axe incomplete")
        + ". "
        + _must_line(source, r"^axe pages \d+$", "axe pages")
        + ". "
        + _must_line(source, r"^\d+ passed.*$", "pytest summary")
        + ".",
    ]
    for text in texts:
        assert_caption_numbers(text, source)
    return texts


def format_timestamp(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    whole = int(seconds)
    millis = int(round((seconds - whole) * 1000))
    if millis == 1000:
        whole += 1
        millis = 0
    minutes, secs = divmod(whole, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def build_srt(intervals: list[tuple[float, float, str]]) -> str:
    blocks = []
    for index, (start, end, text) in enumerate(intervals, 1):
        blocks.append(
            f"{index}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n"
        )
    return "\n".join(blocks) + "\n"


def build_shotlist(intervals: list[tuple[float, float, str]], timing: dict[str, float]) -> str:
    rows = []
    labels = [
        "Hero. Input, check, and result are on one screen.",
        "Judge URL. The synthetic bill is checked and the dispute letter is filled.",
        "Export letter. The markdown file is the whole page.",
        "Health. Static JSON from GET /health.",
        "Capability matrix page rendered from docs/KIRO-CAPABILITY-MATRIX.md.",
    ]
    for (start, end, text), label in zip(intervals, labels):
        rows.append(
            f"- {start:.1f}s–{end:.1f}s. {label} Caption: {text}"
        )
    duration = intervals[-1][1] if intervals else 0
    hero = timing.get("hero_visible_sec", 0)
    letter = timing.get("letter_visible_sec", 0)
    return (
        "# Shot list\n\n"
        "Silent screen recording of the local demo. Synthetic fixtures only. "
        "The script does not record a microphone and does not synthesize speech. "
        f"Duration {duration:.1f}s, which is under 180s. "
        f"The hero is visible at {hero:.1f}s. "
        f"The dispute letter is visible at {letter:.1f}s.\n\n"
        "Caption numbers are copied from demo/measurements.txt. "
        "That file is the stdout of evals/run_gold_and_holdout.py, "
        "the contrast count in scripts/record_demo.py, gallery/axe-report.json, "
        "and demo/pytest-last.txt.\n\n"
        + "\n".join(rows)
        + "\n"
    )


def _axe(page) -> dict:
    page.add_script_tag(path=str(AXE))
    return page.evaluate(
        """() => axe.run({ resultTypes: ['violations', 'incomplete'] })"""
    )


def _sync_gitignore(size: int) -> None:
    text = GITIGNORE.read_text(encoding="utf-8") if GITIGNORE.is_file() else ""
    if size > VIDEO_LIMIT:
        if "demo/raw-walkthrough.webm" not in text:
            suffix = "" if text.endswith("\n") or not text else "\n"
            GITIGNORE.write_text(text + suffix + GITIGNORE_BLOCK, encoding="utf-8")
        return
    cleaned = text.replace(GITIGNORE_BLOCK, "")
    if cleaned != text:
        GITIGNORE.write_text(cleaned, encoding="utf-8")


def record(captions: list[str]) -> tuple[list[tuple[float, float, str]], dict[str, float]]:
    if not AXE.is_file():
        raise SystemExit(f"missing {AXE}")
    from playwright.sync_api import sync_playwright

    httpd = make_server(0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address
    base = f"http://{host}:{port}"
    DEMO.mkdir(parents=True, exist_ok=True)
    intervals: list[tuple[float, float, str]] = []
    timing = {"hero_visible_sec": 0.0, "letter_visible_sec": 0.0}
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
            with tempfile.TemporaryDirectory(prefix="grave-truth-video-") as temp:
                context = browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    record_video_dir=temp,
                    record_video_size={"width": 1280, "height": 720},
                    reduced_motion="reduce",
                )
                page = context.new_page()
                page.set_default_timeout(15000)
                errors: list[str] = []
                page.on("pageerror", lambda exc: errors.append(str(exc)[:300]))
                video = page.video
                clock = time.monotonic()

                def hold(seconds: float) -> None:
                    page.wait_for_timeout(int(seconds * 1000))

                def elapsed() -> float:
                    return time.monotonic() - clock

                page.goto(base + "/", wait_until="domcontentloaded")
                page.wait_for_selector("#hero")
                timing["hero_visible_sec"] = round(elapsed(), 1)
                start = 0.0
                hold(6)
                intervals.append((start, round(elapsed(), 3), captions[0]))

                start = elapsed()
                page.goto(base + "/?judge=1", wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => document.querySelector('#artifact').textContent.toLowerCase().includes('not found')"
                )
                timing["letter_visible_sec"] = round(elapsed(), 1)
                page.locator("#artifact").scroll_into_view_if_needed()
                hold(12)
                intervals.append((round(start, 3), round(elapsed(), 3), captions[1]))

                start = elapsed()
                # The export route sends Content-Disposition: attachment, so a
                # navigation downloads the file instead of showing it. Fetch the
                # same bytes and put them on the page.
                markdown = page.evaluate(
                    """async () => {
                      const response = await fetch('/api/export?app=eob&format=markdown');
                      if (!response.ok) throw new Error('export failed');
                      return await response.text();
                    }"""
                )
                escaped = (
                    markdown.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                )
                page.set_content(
                    "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
                    "<title>Export letter</title>"
                    f"<link rel=\"stylesheet\" href=\"{base}/style.css\"></head>"
                    "<body><article class=\"matrix\"><h1>Synthetic dispute letter</h1>"
                    f"<pre id=\"letter\">{escaped}</pre></article></body></html>",
                    wait_until="domcontentloaded",
                )
                page.wait_for_function(
                    "() => document.querySelector('#letter').textContent.toLowerCase().includes('not found')"
                )
                hold(8)
                intervals.append((round(start, 3), round(elapsed(), 3), captions[2]))

                start = elapsed()
                page.goto(base + "/health", wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => document.body.innerText.includes('unimplemented')"
                )
                hold(8)
                intervals.append((round(start, 3), round(elapsed(), 3), captions[3]))

                start = elapsed()
                page.goto(base + "/kiro.html", wait_until="domcontentloaded")
                page.wait_for_selector("table")
                page.wait_for_function("() => document.body.innerText.includes('0 of 17')")
                axe = _axe(page)
                if axe["violations"] or axe["incomplete"]:
                    context.close()
                    browser.close()
                    raise SystemExit(
                        "matrix page axe "
                        f"violations={len(axe['violations'])} incomplete={len(axe['incomplete'])} "
                        + json.dumps(
                            [
                                {"id": item["id"], "impact": item.get("impact")}
                                for item in axe["violations"] + axe["incomplete"]
                            ]
                        )
                    )
                hold(8)
                page.evaluate("() => window.scrollTo(0, document.body.scrollHeight / 2)")
                hold(8)
                page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                hold(8)
                intervals.append((round(start, 3), round(elapsed(), 3), captions[4]))

                if errors:
                    context.close()
                    browser.close()
                    raise SystemExit("page errors: " + "; ".join(errors))
                if intervals[-1][1] > 180:
                    context.close()
                    browser.close()
                    raise SystemExit(f"recording is {intervals[-1][1]:.1f}s, over 180s")
                context.close()
                if video is None:
                    browser.close()
                    raise SystemExit("Playwright did not open a video")
                video.save_as(str(VIDEO))
                browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
    return intervals, timing


def main() -> int:
    source = collect_measurements()
    captions = caption_texts(source)
    intervals, timing = record(captions)
    for _start, _end, text in intervals:
        assert_caption_numbers(text, source)
    MEASUREMENTS.write_text(source, encoding="utf-8")
    TIMING.write_text(
        "hero_visible_sec {hero_visible_sec}\nletter_visible_sec {letter_visible_sec}\n".format(
            **timing
        ),
        encoding="utf-8",
    )
    CAPTIONS.write_text(build_srt(intervals), encoding="utf-8")
    SHOTLIST.write_text(build_shotlist(intervals, timing), encoding="utf-8")
    size = VIDEO.stat().st_size
    _sync_gitignore(size)
    print(f"wrote {VIDEO} ({size} bytes)")
    print(f"wrote {CAPTIONS}")
    print(f"wrote {SHOTLIST}")
    print(TIMING.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
