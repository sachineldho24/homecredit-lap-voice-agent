"""Pull voice test calls from Retell: transcript + recording + public log + cost.

Usage:
    python -I fetch_calls.py                 # list recent ended calls for both agents
    python -I fetch_calls.py --save          # also write 04_Transcripts/calls/<call_id>.md and download audio
Map a call to a scenario afterwards by renaming the file (e.g. 04_agricultural.md).
"""
import argparse
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")
from retell_api import AGENTS, call  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "04_Transcripts" / "calls"
AUDIO = ROOT / "03_Recordings" / "audio"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true")
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()
    body = {"filter_criteria": {"agent": [{"agent_id": a} for a in AGENTS.values()],
                                "call_status": {"type": "enum", "op": "in", "value": ["ended"]}},
            "sort_order": "ascending", "limit": args.limit}
    items = call("POST", "/v3/list-calls", body).get("items", [])
    names = {v: k for k, v in AGENTS.items()}
    total = 0.0
    for it in items:
        c = call("GET", f"/v2/get-call/{it['call_id']}")
        when = datetime.fromtimestamp(c["start_timestamp"] / 1000).strftime("%Y-%m-%d %H:%M")
        cost = ((c.get("call_cost") or {}).get("combined_cost") or 0) / 100
        total += cost
        dur = (c.get("duration_ms") or 0) / 1000
        first_user = next((t["content"] for t in c.get("transcript_object") or [] if t.get("role") == "user"), "")
        print(f"{when} | {names.get(c['agent_id'], c['agent_id'])} | {dur:5.0f}s | ${cost:.2f} | {c.get('disconnection_reason')} | {c['call_id']} | {first_user[:60]!r}")
        already = OUT.exists() and any(c['call_id'] in f.read_text(encoding='utf-8') for f in OUT.glob('*.md'))
        if args.save and not already:
            OUT.mkdir(parents=True, exist_ok=True)
            lines = [f"# Call {c['call_id']} — {when} — agent {names.get(c['agent_id'])} v{c.get('agent_version')}",
                     f"Duration {dur:.0f}s · ended: {c.get('disconnection_reason')} · cost ${cost:.2f}",
                     f"Recording: {c.get('recording_url')}", f"Public log: {c.get('public_log_url')}", "",
                     "Expected: ... · Actual: ... · Result: PASS/FAIL", ""]
            for t in c.get("transcript_object") or []:
                who = {"agent": "Agent", "user": "Customer"}.get(t.get("role"), t.get("role"))
                lines.append(f"**{who}:** {t.get('content', '').strip()}  ")
            for tc in c.get("transcript_with_tool_calls") or []:
                if tc.get("role") == "tool_call_invocation":
                    lines.append(f"\n[tool call: {tc.get('name')}]")
            (OUT / f"{c['call_id']}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
            if c.get("recording_url"):
                AUDIO.mkdir(parents=True, exist_ok=True)
                dest = AUDIO / f"{c['call_id']}.wav"
                if not dest.exists():
                    urllib.request.urlretrieve(c["recording_url"], dest)
    print(f"\n{len(items)} calls, total cost ${total:.2f}")


if __name__ == "__main__":
    main()
