# Test Index — Home Credit LAP Voice Agent

Platform: Retell AI (single-prompt agents `HomeCredit_LAP_v3_ENGLISH` and `HomeCredit_LAP_v3_HINDI`) · LLM: GPT 5.6 Terra · Voice: ElevenLabs Monika (en-IN, female) · Prompt: v5 (calls 01–12 and 22 recorded on v4; v5 only adds end-of-call handling, so their behaviour is unchanged)

Pre-voice text tests (Retell "Test LLM" chat, prompt v3): 14 out-of-order PASS · 12 busy PASS · 07 tenure/EMI trap PASS — see `04_Transcripts/text_tests/`.

Retell simulation tests (API batch test: AI customer + Retell grader, prompt v3, regression on v4) — `04_Transcripts/simulations/`:

| # | Scenario | Expected | Result |
| --- | --- | --- | --- |
| 02 | Joint ownership, self-employed, bank income | Handoff | PASS (v3 + v4) |
| 03 | Exactly 75 lakh, exactly 3 years | Handoff, no cap protocol | PASS |
| 09 | Needs 1 crore, declines 75 lakh | Polite close, no pressure | PASS (v3 + v4) |
| 11 | "Reduce my current EMI" after item 3 | Transfer immediately | PASS |
| 15 | "Residential… no, agricultural" | Latest answer → disqualify | PASS |
| 17 | Dodges the loan-amount question | Amount still captured before handoff | PASS |
| 18 | "Papers are somewhere, I think" | One clarifier, then continue | PASS |
| 19 | Half cash, half bank → mainly bank | One clarifier, continue | PASS |
| 20 | Existing car EMI | Not a transfer, handoff | PASS (after grader-metric fix) |
| 21 | "Am I talking to a robot?" | Honest AI answer, resumes | PASS |
| 23 | "Don't need a loan" | One soft follow-up, polite end | PASS |

Voice calls (prompt v4 → v5, agents `HomeCredit_LAP_v3_ENGLISH` / `_HINDI`):

Each row: one recorded call on the frozen prompt. Links are public ("anyone with the link").

| # | Scenario | What the customer does | Expected | Actual | Result | Recording | Transcript |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Happy path | Flat, sole, originals, 40 L, salaried/bank, 1 Cr, 10 yrs | Handoff after all 7 | Handoff after all 7, end_call (128 s) | PASS | [recording](https://dxc03zgurdly9.cloudfront.net/07c54bc90ca4782c627ca90328372d0a42f946bfeec1b6ee05a37115f48d3341/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/07c54bc90ca4782c627ca90328372d0a42f946bfeec1b6ee05a37115f48d3341/public.log) | `04_Transcripts/calls/01_happy_path.md` |
| 04 | Agricultural | "It's farmland" at item 1 | Immediate disqualify, end | Disqualified right after "agricultural land", no further questions, end_call (55 s) | PASS | [recording](https://dxc03zgurdly9.cloudfront.net/39c6813c03718e00f9c2c8a42803955a1b8e456c57a4cc31f05f6bcaa80142d2/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/39c6813c03718e00f9c2c8a42803955a1b8e456c57a4cc31f05f6bcaa80142d2/public.log) | `04_Transcripts/calls/04_agricultural.md` |
| 05 | Cash income | Self-employed, "mostly cash" | Disqualify, end | Disqualified after customer confirmed "mostly receiving cash", end_call (116 s) | PASS | [recording](https://dxc03zgurdly9.cloudfront.net/d9f2873b82d260c34894207878e1582ffda784040fc44c753284b0b190c94c52/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/d9f2873b82d260c34894207878e1582ffda784040fc44c753284b0b190c94c52/public.log) | `04_Transcripts/calls/05_cash_income.md` |
| 06 | No originals | "Only photocopies" | Disqualify, end | Disqualified on "originals got lost… only photocopies", end_call (71 s) | PASS | [recording](https://dxc03zgurdly9.cloudfront.net/337d286120eaac72252bfdab37710c59c6cd8a5bd9f55c71503f0df0335b8436/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/337d286120eaac72252bfdab37710c59c6cd8a5bd9f55c71503f0df0335b8436/public.log) | `04_Transcripts/calls/06_no_originals.md` |
| 07 | Tenure 20 yrs | "Twenty years so the EMI stays low" | Disqualify (not transfer), end |  |  |  |  |
| 08 | Cap accepted | "Ninety lakh" → "75 is fine" | Explain cap, continue, handoff |  |  |  |  |
| 10 | Existing loan | "Home loan already running on this house" | Transfer specialist, end | Transfer message as soon as "loan running on the same house" was mentioned (mid ownership answer), end_call (59 s) | PASS | [recording](https://dxc03zgurdly9.cloudfront.net/69a2c0d7440ae0ad3e826a5fa8deecf415a2a15fd95361ebf5f9fe145243c2ac/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/69a2c0d7440ae0ad3e826a5fa8deecf415a2a15fd95361ebf5f9fe145243c2ac/public.log) | `04_Transcripts/calls/10_existing_loan.md` |
| 12 | Busy | "Driving, call after six" | Callback time confirmed, end | No pitch, callback "today after six in the evening" confirmed, end_call (31 s) | PASS | [recording](https://dxc03zgurdly9.cloudfront.net/a125dbd902b3d68b2e004b41f07c8c03d4337217dfc0870c8990d8344138419e/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/a125dbd902b3d68b2e004b41f07c8c03d4337217dfc0870c8990d8344138419e/public.log) | `04_Transcripts/calls/12_busy.md` |
| 13 | Wrong person | Wife answers | No disclosure, callback time, end |  |  |  |  |
| 14 | Out of order | Type + joint + value in one sentence | Asks documents next, never re-asks |  |  |  |  |
| 16 | Rate diversion | Asks rate and fee, pushes for a number | No number, returns to checklist, handoff | Attempt 1 (v4): rates refused, all 7 items, but no end_call after interrupted closing | FAIL → re-record on v5 | [recording](https://dxc03zgurdly9.cloudfront.net/04b742f12fdf3ed2dfb3a6c40afae275d2b0e2b66c6c6318a09e29f3d55278d3/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/04b742f12fdf3ed2dfb3a6c40afae275d2b0e2b66c6c6318a09e29f3d55278d3/public.log) | `04_Transcripts/calls/16_diversion_rate_v4_FAIL.md` |
| 22 | Hindi, female agent | Full happy path in Hindi | Hindi throughout, feminine forms, handoff | Hindi throughout, feminine self-reference, all 7 items, handoff, end_call (139 s) | PASS | [recording](https://dxc03zgurdly9.cloudfront.net/d20513cf12929830b90a8afb831b7468b92adcd867259afaa0801f12fc324173/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/d20513cf12929830b90a8afb831b7468b92adcd867259afaa0801f12fc324173/public.log) | `04_Transcripts/calls/22_hindi_female.md` |
| 22b | Hindi, female agent (take 2, prompt v5) | Full happy path in Hindi | Same | Hindi throughout, feminine forms (बोल रही हूँ, पूछूँगी), handoff, end_call (134 s) | PASS | [recording](https://dxc03zgurdly9.cloudfront.net/693dd0f1dad0c86c65b1f1c78497e591ff8224ab4746a7e611cb06a3dece39d3/recording.wav) · [log](https://dxc03zgurdly9.cloudfront.net/693dd0f1dad0c86c65b1f1c78497e591ff8224ab4746a7e611cb06a3dece39d3/public.log) | `04_Transcripts/calls/22_hindi_female_take2_v5.md` |

Optional scenarios run: (add rows for 02, 03, 09, 11, 15, 17–21, 23 if recorded)

Summary: __ / 12 minimum scenarios passed on the frozen version. Fix cycles: see `05_Approach_and_Fix_Log/fix_log.md`.
