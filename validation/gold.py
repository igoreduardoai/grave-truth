"""Run the existing pytest and gold evals and parse their own summaries."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def parse_pytest_summary(text: str) -> dict:
    passed = _last_int(r"(\d+) passed", text)
    failed = _last_int(r"(\d+) failed", text)
    skipped = _last_int(r"(\d+) skipped", text)
    errors = _last_int(r"(\d+) error", text)
    return {
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "errors": errors,
        "ok": (failed or 0) == 0 and (errors or 0) == 0 and passed is not None,
    }


def parse_eval_summary(text: str) -> dict:
    match = re.search(r"(\d+)/(\d+) passed", text)
    if not match:
        return {"passed": None, "total": None, "ok": False}
    passed, total = int(match.group(1)), int(match.group(2))
    return {"passed": passed, "total": total, "ok": passed == total and total > 0}


def run_gold(root: Path) -> dict:
    pytest_run = _run([sys.executable, "-m", "pytest", "-q"], root)
    eval_run = _run([sys.executable, "evals/run_evals.py"], root)
    pytest_summary = parse_pytest_summary(pytest_run["stdout"] + "\n" + pytest_run["stderr"])
    eval_summary = parse_eval_summary(eval_run["stdout"] + "\n" + eval_run["stderr"])
    return {
        "layer": "pytest_and_gold",
        "exercised": True,
        "pytest": {**pytest_summary, "exit_code": pytest_run["exit_code"]},
        "gold": {**eval_summary, "exit_code": eval_run["exit_code"]},
        "ok": pytest_run["exit_code"] == 0 and eval_run["exit_code"] == 0 and pytest_summary["ok"] and eval_summary["ok"],
    }


def _run(argv: list[str], root: Path) -> dict:
    completed = subprocess.run(argv, cwd=root, capture_output=True, text=True, check=False)
    return {
        "exit_code": completed.returncode,
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
    }


def _last_int(pattern: str, text: str) -> int | None:
    found = re.findall(pattern, text)
    if not found:
        return None
    return int(found[-1])
