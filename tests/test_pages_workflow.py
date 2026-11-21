"""GitHub Pages is a manual workflow. This test does not run it."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pages_workflow_is_manual_and_builds_the_static_site():
    text = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch" in text
    assert "python3 scripts/build_static.py" in text
    assert "actions/upload-pages-artifact" in text
    assert "actions/deploy-pages" in text
    for banned in ("pull_request", "push:", "schedule:", "workflow_run", "repository_dispatch"):
        assert banned not in text
