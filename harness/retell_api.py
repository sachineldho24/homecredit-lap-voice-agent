"""Minimal Retell API helper. Reads RETELL_API_KEY from harness/.env; never prints it."""
import json, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "https://api.retellai.com"
AGENTS = {"en": "agent_e8672f0cac9e2afe5be66d21fe", "hi": "agent_6f2337fe3f8551023b4f8bd9e5"}


def key():
    for line in (HERE / ".env").read_text(encoding="utf-8-sig").splitlines():
        if line.strip().startswith("RETELL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("RETELL_API_KEY missing in harness/.env")


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={
        "Authorization": "Bearer " + key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} on {method} {path}: {e.read()[:500]!r}")
