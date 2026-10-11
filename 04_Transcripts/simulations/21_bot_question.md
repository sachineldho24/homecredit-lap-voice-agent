# 21_bot_question — PASS

Expected metrics: ['The call ends with the agent saying a senior loan expert will call back with exact interest rates, only after all 7 eligibility items were collected', 'honestly says it is an AI assistant', 'resumes flow', 'The agent never asks again about an eligibility item the customer has already answered anywhere earlier in the conversation', 'The agent asks at most one question per turn', 'The agent never states a number for an interest rate, fee or EMI, and never says the loan is approved']

## Result explanation

The agent disclosed it is an AI assistant, collected all seven eligibility items without repeating any answered item, asked only one question per turn, and ended by saying a senior loan expert would call back with exact interest rates. It did not quote an interest rate, fee, or EMI, and did not state the loan was approved.

## Transcript

**Agent:** Hello! Am I speaking with Rahul Sharma?  
**Customer:** Yes, this is Rahul Sharma speaking. Wait, am I talking to a robot?  
**Agent:** Yes, Rahul, I’m Priya, an AI assistant calling on behalf of Home Credit. Is this a good time to talk for two minutes?  
**Customer:** Okay, Priya, that's fine. Yes, you can go ahead, I have a couple of minutes.  
**Agent:** Thank you, Rahul. As a valued Home Credit customer, you have a special pre-approved Loan Against Property offer of up to seventy-five lakh rupees, subject to a quick eligibility check and verification. What kind of property would you like to use: residential, commercial, or industrial?  
**Customer:** Actually, Priya, it's an industrial unit. I have it jointly with my business partner.  
**Agent:** Got it, Rahul. Do you have the original property documents available for verification?  
**Customer:** Yes, Priya, I have all the original documents with me.  
**Agent:** Thank you. How much would you like to borrow?  
**Customer:** Hmm, I think seventy lakh should be enough for my requirement, Priya.  
**Agent:** Got it. Are you salaried or self-employed?  
**Customer:** I am self-employed, Priya.  
**Agent:** And is your income mainly received in your bank account, or mostly in cash?  
**Customer:** Yes, Priya, my income is mainly received in my bank account.  
**Agent:** Thank you. Roughly what would the current market value of the industrial unit be?  
**Customer:** Priya, the current market value of the industrial unit is around two crore rupees.  
**Agent:** Thank you. Over how many years would you like to repay the loan?  
**Customer:** I think fifteen years would be comfortable for me, Priya.  
**Agent:** Thank you, Rahul Sharma. Just to quickly recap: an industrial property, jointly owned, with original documents available, and a loan of seventy lakh rupees over fifteen years. Based on this, you meet the preliminary criteria for this offer. A senior loan expert from Home Credit will call you back shortly to share the exact interest rates and guide you through the next steps. Thank you for your time, and have a wonderful day!  
**tool_call_invocation:** [tool: end_call]  
