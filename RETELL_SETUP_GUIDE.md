# Retell AI — what is configured, and how to make the test calls

Workspace: **SalesAgents Assignment** (dashboard.retellai.com). Both agents were built and checked on 11 Oct 2026.

## Agents

| Setting | `HomeCredit_LAP_v3_ENGLISH` | `HomeCredit_LAP_v3_HINDI` |
| --- | --- | --- |
| Type | Single Prompt | Single Prompt (duplicate) |
| Prompt | `01_System_Prompt/system_prompt.md` **v5** (deployed via API, verified identical by hash) | same v5 |
| LLM | GPT 5.6 Terra (Retell "recommended"; no temperature setting exposed) | same |
| Voice | ElevenLabs **Monika (en-IN)**, female → matches `agent_gender = female` | same |
| Speech language | English (India) | Hindi (India) |
| Welcome | AI speaks first, custom: `Hello! Am I speaking with {{customer_name}}?` | `नमस्ते! क्या मेरी बात {{customer_name}} जी से हो रही है?` |
| Functions | `end_call` (built-in) | same |
| Default dynamic variables | all 11 (see `variables_test_values.md`), `language_to_speak = English` | same, `language_to_speak = Hindi` |
| Interruption sensitivity | 0.9 (barge-in works) | same |
| End call on silence | 30 s | 30 s |
| Max call duration | 6.0 min (protects credits) | 6.0 min (carried over by the duplicate, confirmed via API) |
| Data storage | Everything, keep forever; secure (expiring) URLs **off** | same |

Cost estimate shown by Retell: about $0.16–0.25 per minute. The $10 trial credit covers the 12 required calls (~36 min) with a little room for re-takes. Keep calls short and skip optional scenarios if credits get low.

## Before each calling session
1. Open the ENGLISH agent → Security & fallback settings → Default Dynamic Variables → update `current_date`, `current_day`, `current_time` to now → Save.
2. Use a quiet room and headphones (prevents the agent hearing itself).

## Making a test call (you)
1. Open the agent → right-hand test panel → **Test Audio** → start the call and allow the microphone.
2. Follow `02_Test_Index/call_scripts.md` for the scenario. Speak naturally.
3. The agent should hang up by itself at the end (end_call).
4. Note the scenario number and prompt version.

## Getting public links for submission
1. **Call History** (left menu) → open the call → download the recording (.wav) and copy the transcript.
2. Name the file `NN_slug.wav` (e.g. `04_agricultural.wav`).
3. Upload recordings and transcripts to a Google Drive folder → Share → **Anyone with the link → Viewer**.
4. Paste the links into `02_Test_Index/test_index.md`, or send them to Claude to fill in. Check each link in a private window.

## Re-applying a prompt change
Run `python -I harness/push_prompt.py` to deploy `system_prompt.md` to both agents and check by hash. After voice calls, `python -I harness/fetch_calls.py --save` writes every call's transcript, recording URL and public log URL to `04_Transcripts/calls/` and downloads the audio to `03_Recordings/audio/`.
