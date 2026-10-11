"""Text-mode pre-test harness for the LAP voice agent prompt.

Simulates each scenario in scenarios.json: an agent LLM (running the system
prompt) talks to a customer-simulator LLM, then a judge LLM plus deterministic
checks grade the transcript. Writes results/<id>_<slug>.md and results/report.md.

Usage:
    python -I run_scenarios.py --all
    python -I run_scenarios.py --ids 01 04 14
    python -I run_scenarios.py --minimum --prompt ../01_System_Prompt/versions/v2.md

Keys: OPENAI_API_KEY or ANTHROPIC_API_KEY, from the environment or harness/.env.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_PROMPT = ROOT / "01_System_Prompt" / "system_prompt.md"
RAG_FILE = ROOT / "01_System_Prompt" / "rag_context_sample.md"
RESULTS = HERE / "results"
MAX_TURNS = 22

END_CALL_TOOL_DESC = "End the phone call. Call this right after saying your closing line."


def load_env():
    env_file = HERE / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def rag_block():
    text = RAG_FILE.read_text(encoding="utf-8")
    m = re.search(r"```\n(.*?)```", text, re.S)
    return m.group(1).strip() if m else text


def render_prompt(template, language, agent_gender="female"):
    now = datetime.now()
    values = {
        "company_name": "Home Credit",
        "customer_name": "Rahul Sharma",
        "agent_name": "Priya",
        "agent_gender": agent_gender,
        "current_date": now.strftime("%d %B %Y"),
        "current_day": now.strftime("%A"),
        "current_time": now.strftime("%I:%M %p") + " IST",
        "language_to_speak": language,
        "additional_context_from_rag": rag_block(),
        "conversation_history": "(provided as the conversation messages)",
        "customer_utterance": "(the latest user message)",
    }
    out = template
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", v)
    leftover = re.findall(r"\{\{(\w+)\}\}", out)
    if leftover:
        print(f"warning: unfilled variables {sorted(set(leftover))}", file=sys.stderr)
    return out


def begin_message(language):
    if language == "Hindi":
        return "नमस्ते! क्या मेरी बात Rahul Sharma जी से हो रही है?"
    return "Hello! Am I speaking with Rahul Sharma?"


# ---------------------------------------------------------------- providers

class Provider:
    def __init__(self, agent_model=None, sim_model=None):
        if os.environ.get("OPENAI_API_KEY"):
            from openai import OpenAI
            self.kind = "openai"
            self.client = OpenAI()
            self.agent_model = agent_model or "gpt-4.1"
            self.sim_model = sim_model or "gpt-4.1-mini"
        elif os.environ.get("ANTHROPIC_API_KEY"):
            import anthropic
            self.kind = "anthropic"
            self.client = anthropic.Anthropic()
            self.agent_model = agent_model or "claude-sonnet-5-5"
            self.sim_model = sim_model or "claude-haiku-5-5"
        else:
            sys.exit("No OPENAI_API_KEY or ANTHROPIC_API_KEY found (env or harness/.env).")

    def _retry(self, fn):
        for attempt in range(4):
            try:
                return fn()
            except Exception as e:  # rate limits / transient errors
                if attempt == 3:
                    raise
                print(f"  retrying after error: {e}", file=sys.stderr)
                time.sleep(2 ** attempt * 3)

    def agent_turn(self, system, messages):
        """Returns (spoken_text, ended)."""
        if self.kind == "openai":
            tools = [{"type": "function", "function": {
                "name": "end_call", "description": END_CALL_TOOL_DESC,
                "parameters": {"type": "object", "properties": {}}}}]
            resp = self._retry(lambda: self.client.chat.completions.create(
                model=self.agent_model, temperature=0.3, tools=tools,
                messages=[{"role": "system", "content": system}] + messages))
            msg = resp.choices[0].message
            return (msg.content or "").strip(), bool(msg.tool_calls)
        tools = [{"name": "end_call", "description": END_CALL_TOOL_DESC,
                  "input_schema": {"type": "object", "properties": {}}}]
        resp = self._retry(lambda: self.client.messages.create(
            model=self.agent_model, max_tokens=400, temperature=0.3, system=system,
            tools=tools, messages=messages))
        text = " ".join(b.text for b in resp.content if b.type == "text").strip()
        ended = any(b.type == "tool_use" and b.name == "end_call" for b in resp.content)
        return text, ended

    def complete(self, system, messages, model=None, max_tokens=600):
        model = model or self.sim_model
        if self.kind == "openai":
            resp = self._retry(lambda: self.client.chat.completions.create(
                model=model, temperature=0.5,
                messages=[{"role": "system", "content": system}] + messages))
            return (resp.choices[0].message.content or "").strip()
        resp = self._retry(lambda: self.client.messages.create(
            model=model, max_tokens=max_tokens, temperature=0.5, system=system,
            messages=messages))
        return " ".join(b.text for b in resp.content if b.type == "text").strip()


# ---------------------------------------------------------------- simulation

SIM_SYSTEM = """You are role-playing a real Indian customer receiving a phone call. Stay in character.
{persona}
Speaking style: natural spoken sentences, occasional fillers (umm, haan, actually), never robotic one-word answers unless natural.
Only answer what the caller asks (plus anything your persona says to volunteer). Keep each reply to 1-2 sentences.
Output ONLY the words you say. If the caller has clearly ended the call (said goodbye), output exactly: [HANGUP]"""


def simulate(provider, system_prompt, scenario):
    lang = scenario["language"]
    first = begin_message(lang)
    transcript = [("Agent", first)]
    agent_msgs = [{"role": "assistant", "content": first}]
    ended = False
    for _ in range(MAX_TURNS):
        sim_msgs = [{"role": "user" if s == "Agent" else "assistant", "content": t}
                    for s, t in transcript]
        cust = provider.complete(SIM_SYSTEM.format(persona=scenario["persona"]), sim_msgs)
        if "[HANGUP]" in cust or not cust:
            transcript.append(("Customer", "[hangs up]"))
            break
        transcript.append(("Customer", cust))
        agent_msgs.append({"role": "user", "content": cust})
        text, ended = provider.agent_turn(system_prompt, agent_msgs)
        if text:
            transcript.append(("Agent", text))
            agent_msgs.append({"role": "assistant", "content": text})
        if ended:
            transcript.append(("System", "[agent called end_call]"))
            break
    return transcript, ended


# ---------------------------------------------------------------- grading

JUDGE_SYSTEM = """You grade a transcript of an AI loan-qualification phone call against business rules.
Rules: 7 items in order (property type; ownership; original documents; loan amount <=75 lakh; occupation + income mode; market value; tenure 3-15 years).
Disqualify immediately on agricultural property, no original documents, cash income, tenure outside 3-15 years.
Existing loan on the property or wanting to reduce EMI -> loan transfer specialist message, end call.
>75 lakh -> explain limit, ask to proceed with 75 lakh. Busy -> take callback time, end. Wrong person -> no offer disclosure.
Handoff to senior loan expert only after all 7 items captured. Never invent interest rates/fees. Never re-ask an item already answered.
One question per agent turn.

Return ONLY JSON:
{"outcome": "HANDOFF|DISQUALIFY|TRANSFER|CALLBACK|DECLINED_CAP|NOT_INTERESTED|INCOMPLETE",
 "must_checks": [{"check": "...", "pass": true, "evidence": "..."}],
 "violations": ["re-asked item X at turn N", ...],
 "summary": "one sentence"}"""


def deterministic_checks(transcript, scenario, ended):
    issues = []
    agent_lines = [t for s, t in transcript if s == "Agent"]
    for i, line in enumerate(agent_lines):
        if line.count("?") > 1:
            issues.append(f"agent turn {i + 1} has {line.count('?')} question marks")
        if re.search(r"\d+(\.\d+)?\s*(%|percent|per cent|pratishat)", line, re.I):
            issues.append(f"agent turn {i + 1} states a percentage: {line[:80]!r}")
        if re.search(r"(?<!pre-)(?<!pre )\bapproved\b", line, re.I) and i < len(agent_lines) - 1:
            issues.append(f"agent turn {i + 1} says 'approved' before closing")
    if not ended:
        issues.append("end_call was never called")
    if scenario["language"] == "Hindi":
        joined = " ".join(agent_lines)
        if re.search(r"(raha hoon|sakta hoon|karta hoon|deta hoon|samajh gaya|poochunga|"
                     r"रहा हूँ|सकता हूँ|करता हूँ|देता हूँ|समझ गया|पूछूँगा)", joined):
            issues.append("masculine self-reference found for female agent")
    return issues


def grade(provider, transcript, scenario, ended):
    text = "\n".join(f"{s}: {t}" for s, t in transcript)
    user = (f"Scenario: {scenario['slug']}\nExpected outcome: {scenario['expected']}\n"
            f"Must checks: {json.dumps(scenario['must'])}\n\nTranscript:\n{text}")
    raw = provider.complete(JUDGE_SYSTEM, [{"role": "user", "content": user}],
                            model=provider.agent_model, max_tokens=1200)
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        judged = json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        judged = {}
    det = deterministic_checks(transcript, scenario, ended)
    outcome_ok = judged.get("outcome") == scenario["expected"]
    musts_ok = all(c.get("pass") for c in judged.get("must_checks", [])) if judged else False
    passed = outcome_ok and musts_ok and not judged.get("violations") and not det
    return passed, judged, det


def write_result(scenario, transcript, passed, judged, det, prompt_name):
    path = RESULTS / f"{scenario['id']}_{scenario['slug']}.md"
    lines = [f"# {scenario['id']} {scenario['slug']} — {'PASS' if passed else 'FAIL'}",
             f"Prompt: `{prompt_name}` · Expected: {scenario['expected']} · "
             f"Judged: {judged.get('outcome', '?')}", "", "## Transcript", ""]
    lines += [f"**{s}:** {t}  " for s, t in transcript]
    lines += ["", "## Checks", ""]
    for c in judged.get("must_checks", []):
        lines.append(f"- [{'x' if c.get('pass') else ' '}] {c.get('check')} — {c.get('evidence', '')}")
    for v in judged.get("violations", []):
        lines.append(f"- VIOLATION (judge): {v}")
    for d in det:
        lines.append(f"- VIOLATION (deterministic): {d}")
    lines += ["", f"Summary: {judged.get('summary', '')}"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--minimum", action="store_true", help="only the 12 minimum scenarios")
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--prompt", default=str(DEFAULT_PROMPT))
    ap.add_argument("--agent-model")
    ap.add_argument("--sim-model")
    args = ap.parse_args()

    load_env()
    scenarios = json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))
    if args.ids:
        scenarios = [s for s in scenarios if s["id"] in args.ids]
    elif args.minimum:
        scenarios = [s for s in scenarios if s["minimum"]]
    elif not args.all:
        ap.error("choose --all, --minimum or --ids")

    provider = Provider(args.agent_model, args.sim_model)
    template = Path(args.prompt).read_text(encoding="utf-8")
    prompt_name = Path(args.prompt).name
    RESULTS.mkdir(exist_ok=True)

    rows = []
    for sc in scenarios:
        print(f"[{sc['id']}] {sc['slug']} ...", flush=True)
        system = render_prompt(template, sc["language"])
        transcript, ended = simulate(provider, system, sc)
        passed, judged, det = grade(provider, transcript, sc, ended)
        write_result(sc, transcript, passed, judged, det, prompt_name)
        rows.append((sc, passed, judged, det))
        print(f"     {'PASS' if passed else 'FAIL'} (judged {judged.get('outcome', '?')})")

    report = [f"# Harness report — {prompt_name} — {datetime.now():%Y-%m-%d %H:%M}",
              f"Agent model: {provider.agent_model} · Simulator: {provider.sim_model}", "",
              "| # | Scenario | Expected | Judged | Result | Issues |", "|---|---|---|---|---|---|"]
    for sc, passed, judged, det in rows:
        issues = "; ".join(judged.get("violations", []) + det)[:200]
        report.append(f"| {sc['id']} | {sc['slug']} | {sc['expected']} | {judged.get('outcome', '?')} | "
                      f"{'PASS' if passed else 'FAIL'} | {issues} |")
    n = sum(1 for _, p, _, _ in rows if p)
    report += ["", f"**{n}/{len(rows)} passed**"]
    (RESULTS / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"\n{n}/{len(rows)} passed — see results/report.md")


if __name__ == "__main__":
    main()
