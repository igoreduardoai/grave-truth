import importlib.util
import json
import threading
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_walkthrough_prints_both_apps_and_exits_zero(capsys):
    walk = _load("demo_walkthrough", ROOT / "scripts" / "demo_walkthrough.py")
    assert walk.main() == 0
    out = capsys.readouterr().out
    assert "# eob-explainer" in out
    assert "# lease-checker" in out
    assert "Question:" in out
    assert "Answer:" in out
    assert "Quote:" in out
    assert "Result: PASS" in out
    assert "Result: FAIL" not in out
    assert "Qual é o valor do aluguel?" in out
    assert "The pharmacy charge is $42.15." in out
    assert "not a medical device" in out
    cases = json.loads((ROOT / "evals" / "gold_cases.json").read_text(encoding="utf-8"))
    assert f"passed {len(cases)}/{len(cases)}" in out


def test_haunted_api_cites_and_ghosts():
    server = _load("haunted_server", ROOT / "demos" / "haunted" / "server.py")
    cited = server.ask_payload({"app": "eob", "question": "What is the pharmacy charge?"})
    assert cited["verdict"] == "cited"
    assert cited["ghost"] is False
    assert cited["citations"]
    span = cited["citations"][0]
    assert cited["document"][span["start"]:span["end"]] == span["span"]
    assert "$18.40" in span["span"]

    ghost = server.ask_payload({"app": "lease", "mode": "answer", "question": "Qual é o valor do aluguel?"})
    assert ghost["verdict"] == "not_found"
    assert ghost["ghost"] is True
    assert ghost["citations"] == []
    assert ghost["answer"] == "not found"

    swapped = server.ask_payload({"app": "eob", "mode": "reject", "question": "The pharmacy charge is $42.15."})
    assert swapped["verdict"] == "rejected"
    assert swapped["ghost"] is True
    assert swapped["citations"] == []

    accepted = server.ask_payload({"app": "lease", "mode": "reject", "question": "The late fee is $75.00."})
    assert accepted["verdict"] == "accepted"
    assert accepted["ghost"] is False
    assert any("late fee" in item["span"].lower() and "$75.00" in item["span"] for item in accepted["citations"])


def test_haunted_server_serves_page_and_json():
    server = _load("haunted_server", ROOT / "demos" / "haunted" / "server.py")
    httpd = server.make_server(0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address
    try:
        page = urlopen(f"http://{host}:{port}/", timeout=5)
        html = page.read().decode("utf-8")
        assert "ghost-claim" in html or "ghost-host" in html
        css = urlopen(f"http://{host}:{port}/style.css", timeout=5).read().decode("utf-8")
        assert "fadeGhost" in css
        script = urlopen(f"http://{host}:{port}/app.js", timeout=5).read().decode("utf-8")
        assert "mark" in script and "ghost-claim" in script
        body = json.dumps({"app": "lease", "question": "What is the security deposit?"}).encode()
        request = Request(
            f"http://{host}:{port}/api/ask",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        payload = json.loads(urlopen(request, timeout=5).read().decode("utf-8"))
        assert payload["ghost"] is False
        assert "security deposit" in payload["citations"][0]["span"]
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_readme_counts_match_gold_cases_and_stay_honest():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    cases = json.loads((ROOT / "evals" / "gold_cases.json").read_text(encoding="utf-8"))
    counts = {}
    for case in cases:
        counts[case["expect"]] = counts.get(case["expect"], 0) + 1
    assert f"| cited | {counts['cited']} |" in readme
    assert f"| not_found | {counts['not_found']} |" in readme
    assert f"| reject_ungrounded | {counts['reject_ungrounded']} |" in readme
    assert f"| accept_grounded | {counts['accept_grounded']} |" in readme
    assert f"| **Total** | **{len(cases)}** |" in readme
    assert f"{len(cases)}/{len(cases)} passed" in readme
    assert "demos/haunted/server.py" in readme
    assert "scripts/demo_walkthrough.py" in readme
    assert "Skeleton Crew" in readme
    assert "synthetic" in readme.lower()
    assert "not a medical device" in readme
    assert "not legal advice" in readme
    for banned in ("Americanas", "DocMinds", "44 months"):
        assert banned not in readme


def test_walkthrough_hook_and_steering_exist():
    hook = json.loads((ROOT / ".kiro" / "hooks" / "walkthrough-before-demo.json").read_text(encoding="utf-8"))
    assert hook["version"] == "v1"
    prompt = hook["hooks"][0]["action"]["prompt"]
    assert "demo_walkthrough.py" in prompt
    steering = (ROOT / ".kiro" / "steering" / "haunted-demo.md").read_text(encoding="utf-8")
    assert "demo_walkthrough.py" in steering
    assert "before claiming" in steering.lower() or "Before claiming" in steering
    tasks = (ROOT / ".kiro" / "specs" / "demo-apps" / "tasks.md").read_text(encoding="utf-8")
    assert "haunted" in tasks.lower()
    assert "walkthrough" in tasks.lower()
