# Home Credit LAP Qualification: AI Voice Agent

SalesAgents AI hiring assignment (AI Intern, Prompt Engineer). This is a voice agent that calls existing Home Credit customers about a pre-approved Loan Against Property offer of up to ₹75 lakh. It verifies the customer, handles busy customers and wrong people, collects 7 eligibility items in order while remembering answers given out of order, disqualifies immediately when a rule fails, sends existing-loan and EMI-reduction cases to a loan-transfer specialist, applies the 75 lakh cap, and hands qualified leads to a senior loan expert.

**Platform:** Retell AI. There are two single-prompt agents, English and Hindi, running GPT 5.6 Terra with the ElevenLabs "Monika" voice (Indian English, female), plus the built-in `end_call` tool.

**Live site (recordings playable inline, transcripts, prompt):** https://sachineldho24.github.io/homecredit-lap-voice-agent/

## Start here

| What | Where |
| --- | --- |
| **System prompt (final, v5)** | [`01_System_Prompt/system_prompt.md`](01_System_Prompt/system_prompt.md) · all versions in [`versions/`](01_System_Prompt/versions) |
| Variable values used in testing, RAG sample, welcome message | [`01_System_Prompt/`](01_System_Prompt) |
| **Test results, with public recording and log links** | [`02_Test_Index/test_index.md`](02_Test_Index/test_index.md) |
| **Real voice-call transcripts (evidence)** | [`04_Transcripts/calls/`](04_Transcripts/calls) · full call log: [`04_Transcripts/call_log.md`](04_Transcripts/call_log.md) |
| Call recordings (.wav) | [`03_Recordings/audio/`](03_Recordings/audio), also linked publicly in the call log |
| Retell simulation tests (AI customer + Retell grader) | [`04_Transcripts/simulations/`](04_Transcripts/simulations) |
| Text-chat tests on the deployed agent | [`04_Transcripts/text_tests/`](04_Transcripts/text_tests) |
| Approach note and fix log | [`05_Approach_and_Fix_Log/`](05_Approach_and_Fix_Log) |
| Scripts used to call the Retell API | [`harness/`](harness) |

## How the prompt works

The prompt is a state machine written in plain language. On every turn the agent works through five steps:

1. **Extract** every fact from the customer's words, from anywhere in the call.
2. **Check stop conditions** in a fixed priority order: busy → wrong person → loan transfer → disqualifier → 75 lakh cap → side question.
3. **Update** the hidden 7-item checklist.
4. **Clarify** an ambiguous answer with one question; it never assumes.
5. **Ask only the first unanswered item**, one question per turn.

The handoff to the senior loan expert is allowed only after all 7 items are answered and passed. The prompt never invents rates, fees or eligibility thresholds. It also sets a strict agent gender (including Hindi verb forms), the call language, the RAG-only product facts, and natural speech handling for fillers, corrections, interruptions and numbers spoken in lakh and crore.

## Testing summary

| Layer | Scope | Result |
| --- | --- | --- |
| Retell "Test LLM" text chat | Out-of-order answers, busy, tenure/EMI trap | Found the re-asking bug (v2) → fixed in v3 → all pass |
| Retell batch simulations (API) | 11 scenarios not covered by voice calls | 11/11 pass; transcripts led to fix v4 |
| **Recorded voice calls** | Happy path, agricultural, cash income, no originals, existing loan, busy, Hindi ×2, rate diversion | 8 pass; 1 failure (no hang-up after an interrupted closing) → fixed in v5 |

Every failure is traced to the exact turn and root cause in the [fix log](05_Approach_and_Fix_Log/fix_log.md).

## Reproduce

```bash
echo RETELL_API_KEY=key_xxx > harness/.env
python -I harness/push_prompt.py          # deploy the prompt to both agents and verify by hash
python -I harness/retell_batch.py --ids 02 09   # run scenarios as Retell simulations
python -I harness/fetch_calls.py --save   # pull call transcripts and recordings
```
