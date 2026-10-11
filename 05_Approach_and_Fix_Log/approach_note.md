# Approach Note — Home Credit LAP Qualification Voice Agent

## 1. The problem as I framed it
The hard part of this brief isn't asking seven questions. It's asking them in order while customers answer out of order, interrupt, correct themselves, and drift into side questions. On top of that, a few answers have to stop the call at once. I treated the prompt as a state machine written in natural language, not a script. Every rule in the brief is written out explicitly, and so is every gap I had to fill.

## 2. Architecture
**Stages:** Greeting & identification → (Busy → callback → end) / (Wrong person → callback → end) → Offer → Eligibility check → one of five closings: qualified handoff, disqualification, loan-transfer referral, cap declined, or callback/not interested. Each closing is followed by the `end_call` function.

**Hidden state.** The agent keeps the 7 items (item 5 is split into occupation and income mode), plus flags for verification, transfer, disqualification, a pending clarification and a pending cap offer. It **rebuilds this state from the whole conversation every turn**. That is why a fact mentioned in passing three turns earlier is never asked again.

**Turn algorithm (Section 6 of the prompt): extract → check stop conditions → update → clarify → ask the first missing item.**
Stop conditions run in a fixed priority order: busy → wrong person → transfer → disqualifier → loan cap → side question. Making the order explicit removes ambiguity when one sentence triggers two rules. For example, "the bank has my originals because of a home loan" is a transfer, not a missing-documents disqualification.

## 3. How each requirement maps to the prompt
| Brief requirement | Prompt section |
| --- | --- |
| Verify customer; busy → callback time | §5 Stages 1–2 |
| Present loyalty offer up to 75 lakh | §5 Stage 3 |
| 7 items, sequential, no re-asking out-of-order answers | §6 turn algorithm, §7 items, Example A |
| Immediate disqualification | §6 step 2d, §9 (complete list of disqualifiers) |
| Transfer switch (existing loan / EMI reduction) | §10 |
| > 75 lakh: explain limit, offer maximum | §11, Example C |
| Handoff only after all 7; go back for skipped items | §13 handoff gate, §6 diversion example |
| 11 variables | §2 (each variable listed with how it is used) |
| agent_gender strictly | §3, Hindi verb forms in both scripts |
| language_to_speak | §3 (switch only on an explicit request) |
| RAG context | §12 (only source of product facts; never invent rates/fees) |
| Natural speech, interruptions, fillers | §4, §8 number normalization, §14 edge cases |

## 4. Decisions where the brief is silent
- **Transfer beats disqualification.** A transfer is a different product, not a failed check.
- **Declining the 75 lakh cap ends the call politely,** worded as "may not fit your requirement," not as ineligibility.
- **A car or personal EMI is not a transfer trigger.** Neither is wanting a low EMI on the *new* loan. Only an existing loan on *this* property, or reducing an EMI the customer already pays, triggers the transfer. I added this after the desk review (fix log v2).
- **Originals "at home" or "with my father" count as available.** "Only photocopies" does not.
- **Ambiguity gets exactly one clarifying question** (vague answer on documents, mixed cash/bank income, "land"). The agent never assumes either way.
- **No invented rules:** no market-value minimum, no LTV check, no rates, fees, EMIs or approval promises. "Approved" is never said before the handoff.
- **Wrong person:** nothing about the offer or the account is disclosed to a third party.
- **Honest AI disclosure** when the customer asks "am I talking to a robot?"

## 5. Voice-specific design
One question per turn. Replies of 1–2 sentences. Amounts in Indian words ("seventy-five lakh"). No lists or symbols. The latest correction wins. The agent re-confirms numbers near the 75 lakh, 3-year and 15-year limits, because ASR errors there would flip an eligibility decision. For Hindi, the prompt asks for Devanagari script, which TTS voices pronounce much better than romanized Hindi, while banking words stay in English as people actually say them.

## 6. Testing method
1. **Desk review.** I traced all 23 scenarios through the prompt sections, which led to four fixes (v1 → v2, see fix log).
2. **Text tests in Retell's "Test LLM" chat.** These ran against the deployed agent (GPT 5.6 Terra) before any voice credits were spent. One failure was found and fixed: the agent re-asked the market value and missed an answer given out of turn, which became v3. The out-of-order, busy and tenure/EMI-trap scenarios then passed on v3. Transcripts are in `04_Transcripts/text_tests/`.
3. **Retell simulation tests (API).** The 11 scenarios not covered by voice calls ran as Retell batch tests, with an AI customer and Retell's grader, against the deployed agent: 11/11 passed. One grader false-negative was fixed by making the metric explicit. The transcripts exposed one small prompt issue, the full name used in closing lines, which became v4; the regression run passed.
4. **Voice calls on Retell AI.** Twelve minimum scenarios cover the happy path, every disqualifier, the transfer, the cap, busy, wrong person, out-of-order answers, a rate diversion and Hindi, all on one frozen prompt version.
5. A local automated harness (`harness/run_scenarios.py`, 23 simulated customers plus an LLM judge) is included for regression runs whenever an API key is available.

## 7. Fix-log highlights
- **v3, the most important fix.** In a 30k-character prompt, the "never re-ask" rule in the middle was not enough. The model re-asked a fact given five turns earlier. I repeated the rule in a short critical-rules block at the top and added a "common mistakes" section at the end that quotes the exact failing turns. The failure did not recur on re-test.
- **v2.** "Twenty years so the EMI stays low" could have triggered the transfer switch. Transfer is now defined by intent, meaning an existing loan on this property or reducing a current EMI, not by the keyword "EMI". This was verified in a text test.
- **v2.** Hindi is written in Devanagari for TTS quality, with gender-specific verb forms listed in both scripts.

## 8. Known limitations
- `conversation_history` and `customer_utterance` are placeholders on Retell, because the platform passes the live transcript as messages. The prompt handles both injection styles.
- ASR quality on Indian-accented numbers depends on the platform. The confirm-near-boundary rule reduces the risk but cannot remove it.
- Callback times and DND requests are spoken back to the customer. In production they would be written to a CRM through a function call.
