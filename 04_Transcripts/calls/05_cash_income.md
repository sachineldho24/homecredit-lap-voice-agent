# 05 Cash income — voice call — prompt v4 — call_0bfff8452e6cf77d84cc8b951cf — 2026-10-11 18:10 — agent en v0
Duration 116s · ended: agent_hangup · cost $0.51
Recording: https://dxc03zgurdly9.cloudfront.net/d9f2873b82d260c34894207878e1582ffda784040fc44c753284b0b190c94c52/recording.wav
Public log: https://dxc03zgurdly9.cloudfront.net/d9f2873b82d260c34894207878e1582ffda784040fc44c753284b0b190c94c52/public.log

Expected: Disqualify, end · Actual: Disqualified after customer confirmed "mostly receiving cash", end_call (116 s) · **Result: PASS**

Checks: shop → commercial, sole owner, originals, 30 L captured once each ✔ · speech-to-text turned "cash" into "dash" and "casualty"; agent re-asked instead of guessing (prompt rule: never guess an eligibility answer) ✔ · disqualified only once "cash" was clear, no market value / tenure questions ✔ · end_call ✔

**Agent:** Hello! Am I speaking with Rahul Sharma?  
**Customer:** Yes. You are.  
**Agent:** This is Priya from Home Credit. Is this a good time to talk for two minutes?  
**Customer:** Yeah. Go ahead.  
**Agent:** Thank you for being a valued Home Credit customer. As a reward for your loyalty, you have a pre-approved Loan Against Property offer of up to seventy-five lakh rupees. What kind of property would you like to use—residential, commercial, or industrial?  
**Customer:** Well, I do have a shop.  
**Agent:** Is the shop solely in your name, or jointly owned with someone?  
**Customer:** No. I'm so alone. I'm of trouble.  
**Agent:** Sorry, I didn't catch that clearly. Is the shop only in your name, or jointly owned with someone?  
**Customer:** Uh, well, it's in my name. I'm just all owner of the shop.  
**Agent:** Do you have the original property documents available for verification?  
**Customer:** Yeah. I do have them.  
**Agent:** How much would you like to borrow?  
**Customer:** Maybe, say, thirty lakhs  
**Agent:** Are you salaried or self-employed?  
**Customer:** Well, I run my own grammar shop.  
**Agent:** And is your income mainly received in your bank account, or mostly in cash?  
**Customer:** Honestly, most of it comes in dash.  
**Agent:** Sorry, I didn't catch that clearly — is your main income credited to your bank account, or mostly received in cash?  
**Customer:** Honestly, most of my income is received in casualty.  
**Agent:** Sorry, I didn't catch that clearly — is your main income credited to your bank account, or mostly received in cash?  
**Customer:** It's mostly receiving cash.  
**Agent:** Thank you for sharing that, Rahul. Since your income is mostly received in cash, you unfortunately don't meet the criteria for this specific offer at this time. I appreciate your time and thank you for being a valued Home Credit customer. Have a great day!  

[tool call: end_call]
