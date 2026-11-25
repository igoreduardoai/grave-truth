"""The gate package states what is already true. It does not invent a pass."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "gate"
BANNED = ("Antler", "Americanas", "DocMinds", "Harbor", "Broadway", "2121")


def test_package_files_do_not_repeat_banned_public_tokens():
    seen = False
    for path in GATE.rglob("*"):
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".txt"}:
            continue
        seen = True
        text = path.read_text(encoding="utf-8")
        for banned in BANNED:
            assert banned not in text, path
    assert seen


def test_human_items_stay_open_and_only_the_deployed_url_is_recorded():
    five = (GATE / "evidence" / "five-second.yaml").read_text(encoding="utf-8")
    assert "unaided: false" in five
    health = (GATE / "evidence" / "demo-health.yaml").read_text(encoding="utf-8")
    # The only hosted URL allowed is the deployed demo (deploy/vercel/README.md, 2026-11-21).
    assert 'url: "https://grave-truth.vercel.app/health"' in health
    assert "hf.space" not in health
    assert "huggingface.co" not in health
    assert (ROOT / "deploy" / "vercel" / "README.md").is_file()
    public = (GATE / "evidence" / "public-text.yaml").read_text(encoding="utf-8")
    assert "private_identity_excluded: true" in public
    validation = (GATE / "evidence" / "validation.yaml").read_text(encoding="utf-8")
    assert "lighthouse_hero:" in validation
    assert "90" not in validation.split("lighthouse_hero:", 1)[1].split("\n", 1)[0]
