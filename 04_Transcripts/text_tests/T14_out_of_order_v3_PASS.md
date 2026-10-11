# Text test (Retell "Test LLM") — Scenario 14 out-of-order + diversion + cap — prompt v3 — PASS
Model: GPT 5.6 Terra · 11 Oct 2026

**Agent:** Hello! Am I speaking with Rahul Sharma?
**Customer:** Yes, this is Rahul. Haan, I have a couple of minutes.
**Agent:** This is Priya from Home Credit. As a valued customer, you have a pre-approved Loan Against Property offer of up to seventy-five lakh rupees; may I go ahead with a few quick questions?
**Customer:** Okay, sounds interesting, go ahead.
**Agent:** To start, what kind of property is it: a residential home or flat, commercial property, or industrial property?
**Customer:** Umm, it's a residential house, jointly owned with my wife, and it's worth about one point two crore.
**Agent:** Do you have the original property documents available for verification?
**Customer:** Yes, the originals are at home. But before that, what's your interest rate? Just give me a rough idea, like nine percent?
**Agent:** The exact interest rate will be shared by our senior loan expert after this quick check. How much would you like to borrow?
**Customer:** I'd need around ninety lakh actually.
**Agent:** This offer goes up to a maximum of seventy-five lakh rupees. Would you like to go ahead with the maximum amount of seventy-five lakh?
**Customer:** Hmm okay, seventy-five is fine, let's go with that.
**Agent:** Are you salaried or self-employed?
**Customer:** I'm salaried, I work at an IT company and my salary comes into my HDFC account.
**Agent:** What repayment period would suit you, between three and fifteen years?
**Customer:** Ten years should be fine.
**Agent:** Thank you, Rahul. Just to recap: it's a residential property jointly owned, with original documents available, and you'd like seventy-five lakh rupees over ten years. Based on this, you meet the preliminary criteria for this offer. A senior loan expert from Home Credit will call you back shortly to share the exact interest rates and guide you through the next steps. Thank you for your time, and have a wonderful day!
[end_call]

Checks: ownership + market value never asked (given out of order) ✔ · occupation + income captured from one sentence ✔ · no rate given when pushed ✔ · cap explained, 75 L accepted ✔ · one question per turn ✔ · recap + handoff + end_call ✔
