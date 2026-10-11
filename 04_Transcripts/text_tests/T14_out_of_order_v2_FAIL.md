# Text test (Retell "Test LLM") — Scenario 14 out-of-order + diversion + cap — prompt v2 — FAIL
Model: GPT 5.6 Terra · 11 Oct 2026

**Agent:** Hello! Am I speaking with Rahul Sharma?
**Customer:** Yes, this is Rahul. Haan, I have a couple of minutes.
**Agent:** This is Priya from Home Credit. As a valued customer, you have a pre-approved Loan Against Property offer of up to seventy-five lakh rupees; may I ask a few quick questions to check eligibility?
**Customer:** Okay, sounds interesting, go ahead.
**Agent:** To start, what kind of property would you use: residential, commercial, or industrial?
**Customer:** Umm, it's a residential house, jointly owned with my wife, and it's worth about one point two crore.
**Agent:** Do you have the original property documents available for verification?
**Customer:** Yes, the originals are at home. But before that, what's your interest rate? Just give me a rough idea, like nine percent?
**Agent:** The exact interest rate will be shared by our senior loan expert once this quick check is done. How much would you like to borrow?
**Customer:** I'd need around ninety lakh actually.
**Agent:** This offer goes up to a maximum of seventy-five lakh rupees. Would you like to go ahead with the maximum amount of seventy-five lakh?
**Customer:** Hmm okay, seventy-five is fine, let's go with that.
**Agent:** Are you salaried or self-employed?
**Customer:** I'm salaried, I work at an IT company and my salary comes into my HDFC account.
**Agent:** Roughly what would the current market value of the property be?   ← FAIL: market value already given in turn 3
**Customer:** Ten years should be fine.
**Agent:** Over how many years would you like to repay the loan?   ← FAIL: tenure just given
**Customer:** I just told you, ten years. And the house is worth about one point two crore, I mentioned that earlier.
**Agent:** My apologies, Rahul Sharma. You're right. Based on the preliminary details, you meet the criteria for this offer. A senior loan expert from Home Credit will call you back shortly to share the exact interest rates and guide you through the next steps. Thank you for your time, and have a wonderful day!
[end_call]

Passed: skipped ownership after multi-fact answer, no rate given when pushed, cap protocol, handoff + end_call.
Failed: re-asked market value; ignored tenure given to a different question. → fixed in v3.
