# Variable Values Used in Testing

These are saved as **Default Dynamic Variables** on both Retell agents (Agent → Security & fallback settings → Default Dynamic Variables), so every test call uses them automatically. They can be overridden per test call with the `{ }` button in the test panel. Retell replaces every `{{name}}` in the prompt and begin message.

| Variable | English test calls | Hindi test call | Notes |
| --- | --- | --- | --- |
| company_name | Home Credit | Home Credit | |
| customer_name | Rahul Sharma | Rahul Sharma | Change for variety if desired; never hardcoded in the prompt |
| agent_name | Priya | Priya | |
| agent_gender | female | female | Must match the selected voice |
| current_date | 11 October 2026 | 11 October 2026 | Update to the actual call date |
| current_day | Sunday | Sunday | Update to the actual call day |
| current_time | 5:00 PM IST (default on ENGLISH agent) | Retell built-in `{{current_time}}` | Update the default before a calling session |
| time_of_day | morning | — | Optional, begin message only |
| language_to_speak | English | Hindi | |
| additional_context_from_rag | contents of `rag_context_sample.md` | same | Paste as one block of text |
| conversation_history | (live call transcript is provided by the platform) | same | Retell already passes the full transcript to the LLM every turn; the prompt says to rely on it if this field is a placeholder |
| customer_utterance | (latest customer turn is provided by the platform) | same | Same as above |

Why `conversation_history` / `customer_utterance` are placeholders on Retell: Retell's single-prompt agent sends the whole call transcript to the LLM as chat messages on every turn, so the model always has both. The prompt (Section 2) handles both cases — a production orchestrator that injects these as strings, and a platform that passes them as messages.
