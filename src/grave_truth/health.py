"""Static health payload. No clock, no model, no credential."""

from __future__ import annotations

import json

HEALTH = {
    "auth": "none",
    "live_model": "unimplemented",
    "mode": "offline",
    "service": "grave-truth",
    "status": "ok",
}

HEALTH_BODY = (json.dumps(HEALTH, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
