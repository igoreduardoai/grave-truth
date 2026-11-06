import json
import os
import subprocess
import sys
from pathlib import Path

from grave_truth.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_cli_prints_eob_citation(capsys):
    assert main(["eob", "What is the patient responsibility?"]) == 0
    out = capsys.readouterr().out
    assert "Found: yes" in out
    assert "Ghost: no" in out
    assert "$42.15" in out
    assert "sample-eob" in out


def test_cli_abstains(capsys):
    assert main(["lease", "How much is the reserved parking fee?"]) == 0
    out = capsys.readouterr().out
    assert "Found: no" in out
    assert "Answer: not found" in out
    assert "Ghost: yes" in out


def test_cli_rejects_swapped_amount(capsys):
    assert main(["reject", "eob", "The billed amount is $180.00."]) == 0
    assert "Rejected: yes" in capsys.readouterr().out


def test_cli_accepts_grounded_claim(capsys):
    assert main(["reject", "lease", "The security deposit is $1,850.00."]) == 0
    assert "Rejected: no" in capsys.readouterr().out


def test_cli_json_and_file_mode(capsys):
    assert main(["--json", "file", "fixtures/sample_eob.txt", "What is the claim number?"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["found"] is True
    assert payload["citations"][0]["doc_id"] == "sample_eob"
    assert "CLM-20481" in payload["answer"]


def test_module_entrypoint():
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    proc = subprocess.run(
        [sys.executable, "-m", "grave_truth", "lease", "What is the security deposit?"],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "security deposit" in proc.stdout
    assert "$1,850.00" in proc.stdout
    assert "not rent" in proc.stdout


def test_app_folders_run():
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    eob = subprocess.run(
        [sys.executable, str(ROOT / "eob-explainer" / "main.py"), "Who is the doctor on this visit?"],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    lease = subprocess.run(
        [sys.executable, str(ROOT / "lease-checker" / "main.py")],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert eob.returncode == 0
    assert "Riverside Clinic" in eob.stdout
    assert lease.returncode == 0
    assert "$1,850.00" in lease.stdout
    assert "Monthly rent" in lease.stdout
