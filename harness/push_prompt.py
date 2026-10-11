"""Push 01_System_Prompt/system_prompt.md to both Retell agents' LLMs and verify by hash."""
import hashlib, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")
from retell_api import AGENTS, call  # noqa: E402

text = (Path(__file__).resolve().parent.parent / "01_System_Prompt" / "system_prompt.md").read_text(encoding="utf-8")
h = lambda t: hashlib.sha256(re.sub(r"\s+", "", t).encode()).hexdigest()[:16]
for k, aid in AGENTS.items():
    llm_id = call("GET", f"/get-agent/{aid}")["response_engine"]["llm_id"]
    call("PATCH", f"/update-retell-llm/{llm_id}", {"general_prompt": text})
    live = call("GET", f"/get-retell-llm/{llm_id}")["general_prompt"]
    print(k, llm_id, "match" if h(live) == h(text) else "MISMATCH", h(live))
