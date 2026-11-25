"""Holdout files stay byte-for-byte. This increment does not edit them."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Recorded before this increment edited anything else.
HOLDOUT_SHA256 = {
    "evals/holdout_cases.json": "5414291a00e63d9d8bdae928e898e47e3f948e715639f491dea1a6c20b51a6cf",
    "evals/holdout_observed.json": "4b74dc65027c3615b39ffd9fea7508702cf9548eaf48788a6fefcdf3b9fcf796",
}


def test_holdout_files_keep_their_checksums():
    for relative, expected in HOLDOUT_SHA256.items():
        digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert digest == expected, relative
