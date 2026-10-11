# 02_joint_self_employed — PASS

Expected metrics: ['The call ends with the agent saying a senior loan expert will call back with exact interest rates, only after these 7 items were collected: (1) property type, (2) sole or joint ownership, (3) original documents available, (4) loan amount, (5) salaried or self-employed AND income received via bank or cash, (6) approximate market value, (7) tenure in years. Income amount is NOT one of the items and must not be required', 'joint ownership not disqualified', 'self-employed with bank income not disqualified', 'The agent never asks again about an eligibility item the customer has already answered anywhere earlier in the conversation', 'The agent asks at most one question per turn', 'The agent never states a number for an interest rate, fee or EMI, and never says the loan is approved']

## Result explanation

All seven required eligibility items were collected before the callback statement. The agent did not request income amount, did not disqualify joint ownership or self-employment with bank income, did not repeat answered eligibility questions, asked one question per turn, and gave no numeric interest rate, fee, EMI, or approval statement. The call ends with a senior loan expert callback for exact interest rates.

## Transcript

**Agent:** Hello! Am I speaking with Rahul Sharma?  
**Customer:** Yes, this is Rahul Sharma speaking. How can I help you today?  
**Agent:** Good afternoon, Rahul. This is Priya from Home Credit. Is this a good time to talk for two minutes?  
**Customer:** Yes, Priya, this is a good time. Please go ahead.  
**Agent:** Thank you for being a valued Home Credit customer, Rahul. You have a special pre-approved Loan Against Property offer of up to seventy-five lakh rupees. Shall we go ahead with a few quick eligibility questions?  
**Customer:** Yes, sure, Priya. Please go ahead and ask your questions. I’m ready.  
**Agent:** To start, what kind of property is it — residential, commercial, or industrial?  
**Customer:** It’s a commercial property, actually. It’s a shop located in the market area.  
**Agent:** Thank you. Is the property solely in your name, or jointly owned with someone?  
**Customer:** It’s jointly owned with my brother.  
**Agent:** Got it. Do you have the original property documents available for verification?  
**Customer:** Yes, I do have the original property documents. They are kept safely in my bank locker. If needed, I can arrange to bring them for verification.  
**Agent:** Thank you. How much would you like to borrow?  
**Customer:** I would like to borrow fifty lakh rupees, Priya.  
**Agent:** Thank you. Are you salaried or self-employed?  
**Customer:** I am self-employed, Priya. I run my own business from this shop.  
**Agent:** And is your income received in your bank account, or mostly in cash?  
**Customer:** My income mostly comes into my current account, Priya. Most of my customers pay by cheque or online transfer, so the payments are credited directly to my account.  
**Agent:** That's helpful. Roughly what would the current market value of the property be?  
**Customer:** The current market value of the shop is around eighty lakh rupees, Priya.  
**Agent:** Thank you. Over how many years would you like to repay the loan?  
**Customer:** I would prefer to repay the loan over twelve years, Priya. That would be most comfortable for me, considering my business and other commitments.  
**Agent:** Thank you, Rahul. Just to quickly recap: a commercial property, jointly owned, with original documents available, and a loan of fifty lakh rupees over twelve years. Based on this, you meet the preliminary criteria for this offer. A senior loan expert from Home Credit will call you back shortly to share the exact interest rates and guide you through the next steps. Thank you for your time, and have a wonderful day!  
**tool_call_invocation:** [tool: end_call]  
