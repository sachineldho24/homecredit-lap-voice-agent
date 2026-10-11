# Call Scripts — what to say on each test call

How to run every call
1. Note the prompt version (e.g. v2) and scenario number before starting.
2. Speak like a real customer: fillers, full sentences, a pause or two. Improvise around the key lines; never answer with a bare "yes"/"no" unless the script says so.
3. After the call, tick the pass checks and write the result into `test_index.md`. If it fails, note the exact turn and tell me — I'll update the prompt.
4. Name the recording `NN_slug` (e.g. `04_agricultural`).

Variables for all English calls: customer_name = Rahul Sharma, agent_name = Priya, agent_gender = female, language_to_speak = English.

---

## Minimum set (must record all 12)

### 01_happy_path — expected: HANDOFF
- "Haan, yes, this is Rahul. Sure, I have a couple of minutes."
- After the offer: "Oh okay, sounds interesting, go ahead."
- Property: "It's a flat, a two BHK in Pune."
- Ownership: "Only in my name."
- Documents: "Yes, the original papers are at home in the cupboard."
- Amount: "Umm, around forty lakh should be enough."
- Occupation / income: "I'm salaried, I work at an IT company." → "Salary comes straight into my HDFC account."
- Value: "I'd say it's worth about one crore."
- Tenure: "Ten years is fine."
- ✅ Pass if: all 7 asked once each, short recap, "senior loan expert will call back with exact interest rates", agent hangs up. ❌ no rate mentioned, no item asked twice.

### 04_agricultural — expected: DISQUALIFY
- Confirm identity, say you can talk, sound interested.
- Property: "Actually it's farmland, agricultural land in my village near Nashik."
- ✅ Pass if: polite "don't meet the criteria for this specific offer at this time", no ownership question afterwards, call ends.

### 05_cash_income — expected: DISQUALIFY
- Shop, sole owner, originals available, thirty lakh.
- Occupation: "I run my own kirana shop." → Income: "Honestly most of it comes in cash only."
- ✅ Pass if: disqualifies (one clarifying question is acceptable), no market value / tenure question, call ends.

### 06_no_originals — expected: DISQUALIFY
- Flat, jointly with wife.
- Documents: "Hmm, the originals got lost when we shifted, I only have photocopies now."
- ✅ Pass if: disqualifies, no loan amount question, call ends.

### 07_tenure_out_of_range — expected: DISQUALIFY
- Answer items 1–6 normally (flat, sole, originals, twenty-five lakh, salaried + bank, seventy lakh).
- Tenure: "I'd want a long time, like twenty years, so the EMI stays low."
- ✅ Pass if: disqualifies on tenure (not a transfer message), does not suggest "fifteen years instead", call ends.

### 08_cap_accepted — expected: HANDOFF
- Commercial office, sole owner, originals available.
- Amount: "I'm looking at around ninety lakh." → after the limit: "Hmm, okay, seventy-five is fine, let's go with that."
- Then salaried + bank, one point four crore, fifteen years.
- ✅ Pass if: explains the 75 lakh maximum, asks to proceed with 75, continues, handoff recap says seventy-five lakh.

### 10_existing_loan — expected: TRANSFER
- Confirm identity, can talk.
- Right after the offer: "Oh okay, but there's already a home loan running on this same house with another bank."
- ✅ Pass if: loan-transfer specialist will contact you shortly, no eligibility questions, call ends.

### 12_busy — expected: CALLBACK
- "Yes, this is Rahul, but I'm driving right now — can you call me after six this evening?"
- ✅ Pass if: no offer pitch, confirms the time (ideally with today's day), call ends.

### 13_wrong_person — expected: CALLBACK (no disclosure)
- Speak as his wife: "He's not at home right now, I'm his wife. What is this regarding?"
- If asked for a time: "Try him tomorrow morning around ten."
- ✅ Pass if: no mention of loan / offer / amount, asks for a good time, call ends.

### 14_out_of_order — expected: HANDOFF
- At the first eligibility question: "It's a residential house, jointly owned with my wife, and it's worth about one point two crore."
- Then: originals at home; sixty lakh; salaried, bank credit; ten years.
- ✅ Pass if: the very next question is about documents; ownership and market value are never asked again.

### 16_diversion_rate — expected: HANDOFF
- Right after the offer: "Before that, what's your interest rate? And is there any processing fee?"
- Push once: "Just give me a rough idea — eight percent, nine percent?"
- Then cooperate: flat, sole, originals, forty lakh, salaried + bank, ninety lakh, eight years.
- ✅ Pass if: no number for rate or fee at any point, returns to the next question in the same turn, handoff.

### 22_hindi_female — expected: HANDOFF (Hindi agent: duplicate agent, language Hindi, Hindi voice)
- "Haan ji, main Rahul bol raha hoon. Haan, baat kar sakte hain."
- "Ghar hai, flat hai." → "Sirf mere naam pe hai." → "Original papers ghar pe rakhe hain."
- "Pachaas lakh chahiye." → "Naukri karta hoon, salary bank mein aati hai."
- "Flat ki value lagbhag ek crore hogi." → "Das saal mein chukana hai."
- ✅ Pass if: agent speaks Hindi throughout, uses feminine forms ("bol rahi hoon", "samajh gayi", "poochungi"), amounts in words, handoff in Hindi.

---

## Optional set (if credits allow)

| # | Slug | Key lines | Expected |
| --- | --- | --- | --- |
| 02 | joint_self_employed | "Shop, jointly with my brother" · "I run a business, payments come to my current account" | HANDOFF |
| 03 | boundaries | Exactly "seventy-five lakh" and "three years" | HANDOFF, no cap protocol |
| 09 | cap_declined | "I need at least one crore" → "No, seventy-five won't work" | Polite close, no pressure |
| 11 | emi_mid_flow | After the documents answer: "Actually I just want to reduce my current EMI" | TRANSFER immediately |
| 15 | correction_to_agri | "It's residential… no wait, it's agricultural land" | DISQUALIFY |
| 17 | skipped_item | When asked the amount, ask about documents/processing instead | Amount still asked before handoff |
| 18 | ambiguous_docs | "The papers are somewhere at home I think, probably" | One clarifier, no assumption |
| 19 | mixed_income | "Half cash, half bank" → "Mainly bank, big clients pay by NEFT" | One clarifier, continues |
| 20 | unrelated_emi | "I already have a car loan EMI, is that a problem?" | Not a transfer, continues |
| 21 | bot_question | Interrupt mid-sentence: "Wait, am I talking to a robot?" | Honest AI answer, resumes |
| 23 | not_interested | "No, I don't need any loan right now, thank you" | At most one soft follow-up, polite end |
