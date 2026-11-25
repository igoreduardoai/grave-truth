"""Specs, steering, the on-save hook, and a keyless MCP config do work."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cite_or_abstain_steering_is_always_on():
    text = (ROOT / ".kiro" / "steering" / "cite-or-abstain.md").read_text(encoding="utf-8")
    assert "inclusion: always" in text
    assert "not found" in text
    assert "number" in text.lower()
    legacy = json.loads((ROOT / ".kiro" / "hooks" / "run-evals.json").read_text(encoding="utf-8"))
    assert ".kiro/steering/cite-or-abstain.md" in legacy["steering"]


def test_workflow_spec_names_the_module_that_builds_the_file():
    specs = ROOT / ".kiro" / "specs" / "workflow-artifact"
    requirements = (specs / "requirements.md").read_text(encoding="utf-8")
    design = (specs / "design.md").read_text(encoding="utf-8")
    tasks = (specs / "tasks.md").read_text(encoding="utf-8")
    assert "not found" in requirements
    assert "DocumentAgent" in design
    assert "src/grave_truth/artifact.py" in tasks
    assert (ROOT / "src" / "grave_truth" / "artifact.py").is_file()
    overview = (ROOT / ".kiro" / "specs" / "grave-truth.md").read_text(encoding="utf-8")
    assert "workflow-artifact" in overview


def test_save_hook_runs_gold_and_holdout_without_editing_holdout():
    hook = json.loads(
        (ROOT / ".kiro" / "hooks" / "gold-holdout-on-save.json").read_text(encoding="utf-8")
    )
    assert hook["version"] == "v1"
    command = hook["hooks"][0]["action"]["command"]
    assert command == "python3 evals/run_gold_and_holdout.py"
    holdout = ROOT / "evals" / "holdout_cases.json"
    observed = ROOT / "evals" / "holdout_observed.json"
    before = holdout.read_bytes(), observed.read_bytes()
    proc = subprocess.run(
        [sys.executable, str(ROOT / "evals" / "run_gold_and_holdout.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "90/90 passed" in proc.stdout
    assert "holdout 7/7" in proc.stdout
    assert (holdout.read_bytes(), observed.read_bytes()) == before


def test_mcp_config_is_keyless_and_points_at_the_fixture_server():
    config = json.loads((ROOT / ".kiro" / "settings" / "mcp.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["grave-truth-fixtures"]
    assert server["command"] == "python3"
    assert server["args"] == ["scripts/fixture_mcp.py"]
    blob = json.dumps(config)
    assert "apiKey" not in blob
    assert "Authorization" not in blob
    assert "token" not in blob.lower()
