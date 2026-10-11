# 19_mixed_income — PASS

Expected metrics: ['The call ends with the agent saying a senior loan expert will call back with exact interest rates, only after all 7 eligibility items were collected', 'asks one clarification on mixed income', 'continues after mainly-bank answer', 'The agent never asks again about an eligibility item the customer has already answered anywhere earlier in the conversation', 'The agent asks at most one question per turn', 'The agent never states a number for an interest rate, fee or EMI, and never says the loan is approved']

## Result explanation

All seven eligibility items were collected before the callback statement: property type, ownership, original documents, loan amount, employment type, income banking status, property value, and tenure (the transcript actually collects eight fields). The agent asks exactly one clarification after mixed income, continues after the mainly-bank answer, does not repeat answered items, asks no more than one question per turn, and gives no numeric interest rate, fee, or EMI and does not claim approval. The agent states that a senior loan expert will call back with exact interest rates.

## Transcript

**Agent:** Hello! Am I speaking with Rahul Sharma?  
**Customer:** Yes, this is Rahul Sharma speaking. How can I help you?  
**Agent:** Good afternoon, Rahul. This is Priya from Home Credit. Is this a good time to talk for two minutes?  
**Customer:** Yes, Priya, this is a good time. Please go ahead, tell me what you need.  
**Agent:** Thank you for being a valued Home Credit customer. You have a special pre-approved Loan Against Property offer of up to seventy-five lakh rupees, subject to a quick eligibility check. Shall we go ahead?  
**Customer:** Okay, sure, you can go ahead with the eligibility check. What details do you need from my side?  
**Agent:** To start, what kind of property is it: residential, commercial, or industrial?  
**Customer:** It's a commercial office property.  
**Agent:** Thank you. Is the property solely in your name, or jointly owned with someone?  
**Customer:** It's solely in my name, Priya.  
**Agent:** Do you have the original property documents available for verification?  
**Customer:** Yes, I have all the original property documents with me.  
**Agent:** How much would you like to borrow?  
**Customer:** I would like to borrow thirty lakh rupees, Priya.  
**Agent:** Are you salaried or self-employed?  
**Customer:** I am self-employed, Priya.  
**Agent:** And is your income mainly received in your bank account, or mostly in cash?  
**Customer:** It's kind of half and half, Priya. Some clients pay me in cash, and some pay directly to my bank account.  
**Agent:** Is your main income credited to your bank account, with proper bank records?  
**Customer:** Yes, mainly the bank, Priya. All my big clients pay by NEFT, so the main income is credited to my bank account.  
**Agent:** Thank you. Roughly what would the current market value of the property be?  
**Customer:** The current market value of the property would be around sixty lakh rupees, Priya.  
**Agent:** Over how many years would you like to repay the loan?  
**Customer:** I would prefer a tenure of seven years for the repayment, Priya. That would be comfortable for me.  
**Agent:** Thank you, Rahul Sharma. Just to recap: it is a commercial property solely owned by you, with original documents available, and you need thirty lakh rupees over seven years. Based on this, you meet the preliminary criteria for this offer. A senior loan expert from Home Credit will call you back shortly to share the exact interest rates and guide you through the next steps. Thank you for your time, and have a wonderful day!  
**Customer:** Thank you so much, Priya. I appreciate your help. I’ll wait for the call from your senior expert. Have a good day!  
**Agent:** Thank you, Rahul. Have a great day!  
**tool_call_invocation:** [tool: end_call]  
