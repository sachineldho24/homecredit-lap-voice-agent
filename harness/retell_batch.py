"""Run scenarios from scenarios.json as Retell simulation tests (batch test API).

Usage:
    python -I retell_batch.py --ids 02 03 09        # create/run selected scenarios
    python -I retell_batch.py --optional            # all non-minimum scenarios
    python -I retell_batch.py --resume <batch_id>   # just poll + collect results

Results: results/retell_batch/<id>_<slug>.md and results/retell_batch/report.md
"""
import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")
from retell_api import AGENTS, call  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "retell_batch"
STATE = OUT / "definitions.json"

UNIVERSAL = [
    "The agent never asks again about an eligibility item the customer has already answered anywhere earlier in the conversation",
    "The agent asks at most one question per turn",
    "The agent never states a number for an interest rate, fee or EMI, and never says the loan is approved",
]
OUTCOME = {
    "HANDOFF": "The call ends with the agent saying a senior loan expert will call back with exact interest rates, only after these 7 items were collected: (1) property type, (2) sole or joint ownership, (3) original documents available, (4) loan amount, (5) salaried or self-employed AND income received via bank or cash, (6) approximate market value, (7) tenure in years. Income amount is NOT one of the items and must not be required",
    "DISQUALIFY": "The agent politely says the customer does not meet the criteria for this offer, asks no further eligibility questions, and ends the call",
    "TRANSFER": "The agent says a loan transfer specialist will contact the customer, asks no further eligibility questions, and ends the call",
    "CALLBACK": "The agent does not pitch the offer, confirms a callback time, and ends the call",
    "DECLINED_CAP": "The agent explains the 75 lakh maximum, asks once whether to proceed with 75 lakh, and after the refusal closes politely without pressure",
    "NOT_INTERESTED": "The agent makes at most one gentle follow-up and then ends the call politely without pressure",
}
SIM_SUFFIX = (" Speak like a real Indian customer on the phone: natural full sentences, occasional fillers. "
              "Only reveal facts when asked unless told to volunteer them. When the agent says goodbye, end the conversation.")


def llm_and_vars():
    agent = call("GET", f"/get-agent/{AGENTS['en']}")
    llm_id = agent["response_engine"]["llm_id"]
    llm = call("GET", f"/get-retell-llm/{llm_id}")
    return llm_id, dict(llm.get("default_dynamic_variables") or {})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--optional", action="store_true")
    ap.add_argument("--resume")
    ap.add_argument("--sim-model", default="gpt-4.1")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    scenarios = {s["id"]: s for s in json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))}
    defs = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}

    llm_id, dvars = llm_and_vars()
    engine = {"type": "retell-llm", "llm_id": llm_id}

    if args.resume:
        batch_id = args.resume
    else:
        ids = args.ids or [i for i, s in scenarios.items() if args.optional and not s["minimum"]]
        if not ids:
            ap.error("choose --ids, --optional or --resume")
        def_ids = []
        for i in ids:
            sc = scenarios[i]
            if sc["language"] != "English":
                sys.exit(f"{i}: only English scenarios run against the ENGLISH agent")
            body = {
                "name": f"{sc['id']}_{sc['slug']}",
                "response_engine": engine,
                "user_prompt": sc["persona"] + SIM_SUFFIX,
                "metrics": [OUTCOME[sc["expected"]]] + sc["must"] + UNIVERSAL,
                "dynamic_variables": dvars,
                "llm_model": args.sim_model,
            }
            if i in defs:
                call("PUT", f"/update-test-case-definition/{defs[i]}", body)
            else:
                defs[i] = call("POST", "/create-test-case-definition", body)["test_case_definition_id"]
            def_ids.append(defs[i])
            print(f"definition {i} {sc['slug']} -> {defs[i]}")
        STATE.write_text(json.dumps(defs, indent=2), encoding="utf-8")
        batch = call("POST", "/create-batch-test", {"test_case_definition_ids": def_ids, "response_engine": engine})
        batch_id = batch["test_case_batch_job_id"]
        (OUT / "last_batch.txt").write_text(batch_id, encoding="utf-8")
        print("batch:", batch_id)

    for _ in range(120):
        b = call("GET", f"/get-batch-test/{batch_id}")
        print(f"  {b['status']}: pass {b['pass_count']} fail {b['fail_count']} error {b['error_count']} / {b['total_count']}", flush=True)
        if b["status"] == "complete":
            break
        time.sleep(15)

    runs, key = [], None
    while True:
        q = f"/v2/list-test-runs/{batch_id}?limit=100" + (f"&pagination_key={key}" if key else "")
        page = call("GET", q)
        runs += page["items"]
        if not page.get("has_more"):
            break
        key = page["pagination_key"]

    rows = []
    for r in sorted(runs, key=lambda r: r["test_case_definition_snapshot"]["name"]):
        name = r["test_case_definition_snapshot"]["name"]
        (OUT / f"{name}.json").write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
        lines = [f"# {name} — {r['status'].upper()}", "", f"Expected metrics: {r['test_case_definition_snapshot']['metrics']}", "",
                 "## Result explanation", "", r.get("result_explanation") or "(none)", "", "## Transcript", ""]
        snap = r.get("transcript_snapshot") or {}
        for t in snap.get("transcript") or snap.get("messages") or []:
            role = t.get("role", "?")
            text = t.get("content") or t.get("text") or (f"[tool: {t.get('name')}]" if t.get("name") else json.dumps(t, ensure_ascii=False))
            lines.append(f"**{ 'Agent' if role in ('agent','assistant') else 'Customer' if role=='user' else role}:** {text}  ")
        (OUT / f"{name}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        rows.append((name, r["status"], (r.get("result_explanation") or "").replace("\n", " ")[:300]))

    rep = [f"# Retell simulation batch {batch_id} — {datetime.now():%Y-%m-%d %H:%M}", "",
           "| Scenario | Result | Explanation |", "|---|---|---|"]
    rep += [f"| {n} | {s.upper()} | {e} |" for n, s, e in rows]
    rep += ["", f"**{sum(1 for _, s, _ in rows if s == 'pass')}/{len(rows)} passed**"]
    (OUT / "report.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
