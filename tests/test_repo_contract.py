import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_kiro_is_not_gitignored_and_hooks_parse():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".kiro" not in ignore
    assert (ROOT / ".kiro").is_dir()
    hooks = list((ROOT / ".kiro" / "hooks").glob("*.json"))
    assert len(hooks) >= 3
    legacy = json.loads((ROOT / ".kiro" / "hooks" / "run-evals.json").read_text(encoding="utf-8"))
    assert "run_evals.py" in legacy["command"]
    v1 = 0
    for path in hooks:
        data = json.loads(path.read_text(encoding="utf-8"))
        if path.name == "run-evals.json":
            continue
        assert data["version"] == "v1"
        assert data["hooks"]
        v1 += 1
    assert v1 >= 2


def test_license_stays_mit():
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert license_text.startswith("MIT License")
    assert "Igor Eduardo" in license_text
    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'license = { text = "MIT" }' in project


def test_specs_and_steering_exist():
    specs = ROOT / ".kiro" / "specs"
    assert (specs / "grave-truth.md").is_file()
    assert (specs / "citation-grounding" / "requirements.md").is_file()
    assert (specs / "citation-grounding" / "design.md").is_file()
    assert (specs / "citation-grounding" / "tasks.md").is_file()
    assert (specs / "demo-apps" / "requirements.md").is_file()
    steering = list((ROOT / ".kiro" / "steering").glob("*.md"))
    assert len(steering) >= 4
    no_invention = (ROOT / ".kiro" / "steering" / "no-invention.md").read_text(encoding="utf-8")
    assert "not found" in no_invention
    assert "not a medical device" in no_invention
    assert "not legal advice" in no_invention
