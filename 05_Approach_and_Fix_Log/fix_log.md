# Prompt Fix Log

Every failure becomes one row and one targeted change. Versions are kept in `01_System_Prompt/versions/`.

Fix loop: find the exact failing turn → name the root cause in one line → make the smallest prompt change → save a new version → re-run the failed scenario and scenario 01 (regression).

| Version | Source | Scenario | What failed / risk (turn and quote) | Root cause | Change made | Re-test |
| --- | --- | --- | --- | --- | --- | --- |
| v1 → v2 | Desk review | 07 tenure, 16 diversion | Customer says "twenty years so the EMI stays low" — "EMI" could fire the transfer switch instead of the tenure disqualifier | Transfer trigger defined by keyword, not intent | Section 10: wanting a low EMI on the *new* loan is explicitly not a transfer trigger; only an existing loan on this property or reducing a current EMI is | Retell text test 07 on v3 → PASS (treated as tenure disqualifier, not transfer) |
| v1 → v2 | Desk review | 13 wrong person | Wife asks "What is this regarding?" — v1 had no answer, so the model might explain the offer | Missing script for a third party's question | Section 5: fixed line "It's regarding their account with {{company_name}} — I'll speak with them directly"; never ask a third party eligibility questions | Voice call 13 (pending) |
| v1 → v2 | Desk review | 22 Hindi | Romanized Hindi ("bol rahi hoon") is mispronounced by most TTS voices | Script choice not specified for TTS | Section 3: Hindi in Devanagari, banking words in English letters, amounts in Hindi words; gender forms listed in both scripts; Example F rewritten; Hindi begin message in Devanagari | Voice call 22 (pending) |
| v1 → v2 | Desk review | 01, 14, 16 | Agent asks "shall we go ahead?" even after the customer has already said "yes, tell me more" — an extra yes/no turn | Offer stage always asked for consent | Stage 3: skip the consent question if interest is already expressed | Seen in text test 07 on v3: agent went straight to item 1 after "Sure, go ahead" → PASS |
| v2 → v3 | Retell Test LLM (GPT 5.6 Terra) | 14 out-of-order | Turn 8: agent asked "Roughly what would the current market value be?" although the customer said "worth about one point two crore" in turn 3; turn 9: customer answered "ten years" to the value question and the agent then asked "Over how many years…?" (transcript `04_Transcripts/text_tests/T14_out_of_order_v2_FAIL.md`) | The no-re-ask rule lived mid-prompt (Section 6); with a 30k-char prompt the model lost track of facts given many turns earlier and of answers given to a different question | Added **Section 0 Critical Rules** at the top (never re-ask; answers count wherever they appear; one question; stop rules; no numbers; first-name address; end_call) and **Section 17 Common Mistakes** at the end with these exact two failures as WRONG/RIGHT examples (primacy + recency) | Re-ran 14 → PASS (`T14_out_of_order_v3_PASS.md`); regression: 12 busy PASS, 07 tenure/EMI trap PASS |
| v2 → v3 | Retell Test LLM | 14 | Agent addressed the customer by full name ("My apologies, Rahul Sharma") | No rule on how to use {{customer_name}} | Critical rule 6: first name with respectful touch ("Rahul", "Rahul ji", "Mr. Sharma") | v3 transcripts use "Rahul" |
| v3 (grader) | Retell simulation batch (11 optional scenarios) | 20 unrelated car EMI | Retell's grader marked FAIL: "did not obtain … income amount" — the agent had in fact collected all 7 items and correctly ignored the car EMI | Test metric, not the prompt: "all 7 eligibility items" was undefined for the grader | Metric now lists the 7 items explicitly and says income amount is not required (no prompt change) | Re-ran 20 → PASS; batch total 11/11 |
| v3 → v4 | Retell simulation batch | 02, 03, 09, 17–21 | Every closing line said "Thank you, Rahul Sharma" — full name, despite critical rule 6 | Closing scripts in Sections 9, 10, 11, 13 literally contained {{customer_name}}, and the model copies scripts verbatim | Scripts now say [first name]; rule 6 says the full name is used only for the identity check | Regression 02 + 09 on v4 → PASS, closings now "Thank you, Rahul" |
| v4 (observed, not changed) | Voice call 12 busy | 12 | Closing line spoken twice in slightly different words before end_call | Likely the platform re-prompted the LLM once before the end_call tool fired; outcome unaffected | Not changed: prompt is frozen at v4 for recorded calls. Candidate v5 fix: "say the closing line once, then call end_call in the same turn" | — |
| v4 → v5 | Voice call 16 attempt 1 (`04_Transcripts/calls/16_diversion_rate_v4_FAIL.md`) + voice call 12 | 16, 12 | Customer cut in during the handoff recap ("you haven't told me any rough interest rate"); agent answered and said goodbye but never called end_call, said goodbye again, then asked "Hello, are you still there?" — the customer had to hang up. Call 12 also had a doubled goodbye | The prompt said to end with end_call but never said it must happen in the same turn as the goodbye, nor what to do when the closing is interrupted; the silence rule ("are you still there?") also fired after a goodbye | Critical rule 7 rewritten (one goodbye + end_call in the same turn, even after an interrupted closing); handoff section: how to handle a question during the recap; silence rule exception after goodbye; Section 17 Mistake 3 quotes this exact call | Simulation 24 on v5: correct single goodbye + end_call (Retell's text simulator cannot barge in mid-sentence, so the interruption itself must be verified by the voice re-record of 16) |
| v5 → v6 |  |  |  |  |  |  |

## Desk review notes (v2), scenario by scenario

Expected behaviour traced through the prompt sections (no LLM API key was available, so the local harness in `harness/` has not been run; Retell's Test LLM chat was used for text tests instead):

| # | Scenario | Section(s) that decide it | Predicted result |
| --- | --- | --- | --- |
| 01 | Happy path | 6 turn algorithm, 7, 13 | Handoff after 7 items, recap, no rate |
| 04 | Agricultural | 6 step 2d, 9 | Immediate disqualify, end_call |
| 05 | Cash income | 7 item 5, 9 | Disqualify (one clarifier only if mixed) |
| 06 | No originals | 7 item 3, 9 | Disqualify; "photocopies only" is explicitly listed |
| 07 | 20-year tenure | 7 item 7, 9, 10 (v2 fix) | Disqualify, no counter-offer |
| 08 | Cap accepted | 11 | Explain limit → record 75 L → continue |
| 10 | Existing loan | 6 step 2c, 10 | Transfer message, end_call, no checklist |
| 12 | Busy | 5 stage 2 | Callback time confirmed with day, end |
| 13 | Wrong person | 5 stage 1 (v2 fix) | No disclosure, callback time, end |
| 14 | Out of order | 6 example, 15 Example A | Next question = documents; ownership/value never re-asked |
| 16 | Rate diversion | 12, Example E | No number given even when pushed, returns to next item |
| 22 | Hindi female | 3 (v2 fix), Example F | Devanagari, feminine forms |

Residual risks to watch in voice tests: ASR mishearing "seventy-five" vs "seventy" (mitigated by the confirm-near-boundary rule in Section 8), and agents adding a second question at handoff ("Anything else I can help with?") — the self-check forbids stacked questions.
