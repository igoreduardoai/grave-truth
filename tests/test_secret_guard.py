import json

from grave_truth.secret_guard import find_secret_paths


def test_blocks_env_and_key_paths():
    payload = json.dumps(
        {
            "tool": {
                "name": "write",
                "input": {"path": "config/.env", "content": "TOKEN=nope"},
            }
        }
    )
    assert find_secret_paths(payload) == ["config/.env"]
    nested = json.dumps({"arguments": {"filePath": "secrets/id_rsa"}})
    assert find_secret_paths(nested) == ["secrets/id_rsa"]
    pem = json.dumps({"target_file": "certs/server.pem"})
    assert find_secret_paths(pem) == ["certs/server.pem"]


def test_allows_source_and_ignores_unparseable_input():
    payload = json.dumps({"path": "src/grave_truth/skeleton.py"})
    assert find_secret_paths(payload) == []
    assert find_secret_paths("not json, mentions .env in prose") == []
    assert find_secret_paths("") == []
