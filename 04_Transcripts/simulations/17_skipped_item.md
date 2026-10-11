# 17_skipped_item — PASS

Expected metrics: ['The call ends with the agent saying a senior loan expert will call back with exact interest rates, only after all 7 eligibility items were collected', 'loan amount is asked and captured before handoff', 'The agent never asks again about an eligibility item the customer has already answered anywhere earlier in the conversation', 'The agent asks at most one question per turn', 'The agent never states a number for an interest rate, fee or EMI, and never says the loan is approved']

## Result explanation

All seven eligibility items were collected before the handoff: property type, ownership, original documents, loan amount, employment type, salary credit mode, property value, and tenure (the transcript actually collects eight). The loan amount was captured before handoff. No eligibility item was re-asked after being answered, and each agent turn asks no more than one question. The agent states no interest-rate, fee, or EMI number and does not claim approval; it only says the customer meets preliminary criteria. The agent says a senior loan expert will call back with exact interest rates before the closing exchange.

## Transcript

**Agent:** Hello! Am I speaking with Rahul Sharma?  
**Customer:** Yes, this is Rahul Sharma speaking. I can talk now.  
**Agent:** Good afternoon, Rahul. This is Priya from Home Credit. As a valued customer, you have a special pre-approved Loan Against Property offer of up to seventy-five lakh rupees. May I quickly check a few details?  
**Customer:** Sure, Priya, you can go ahead and ask whatever details you need.  
**Agent:** Thank you, Rahul. What kind of property would you like to use—residential, commercial, or industrial?  
**Customer:** It's a commercial shop, Priya.  
**Agent:** Got it. Is the shop solely in your name, or jointly owned with someone?  
**Customer:** It's solely in my name.  
**Agent:** Thank you. Do you have the original property documents available for verification?  
**Customer:** Yes, I have all the original property documents available.  
**Agent:** How much would you like to borrow?  
**Customer:** Actually, before I decide on the loan amount, could you please let me know what documents you will need from my side and how long the processing usually takes?  
**Agent:** The expert will need the original property documents, PAN, Aadhaar, six months of bank statements, and your last three salary slips or two years of ITR, depending on your work type. Our senior loan expert will share the exact processing details; roughly how much would you like to borrow?  
**Customer:** Alright, Priya, I would like to borrow thirty-five lakh rupees.  
**Agent:** Thank you. Are you salaried or self-employed?  
**Customer:** I'm salaried, Priya.  
**Agent:** And is your salary credited to your bank account, or do you receive it mostly in cash?  
**Customer:** My salary is credited directly to my bank account every month.  
**Agent:** Roughly what would the current market value of the shop be?  
**Customer:** The current market value of the shop is around seventy lakh rupees.  
**Agent:** Over how many years would you like to repay the loan?  
**Customer:** I would prefer to repay the loan over six years, Priya.  
**Agent:** Thank you, Rahul Sharma. Just to quickly recap: a commercial property, solely owned, original documents available, a loan of thirty-five lakh rupees over six years. Based on this, you meet the preliminary criteria for this offer. A senior loan expert from Home Credit will call you back shortly to share the exact interest rates and guide you through the next steps. Thank you for your time, and have a wonderful day!  
**Customer:** Thank you, Priya. Looking forward to the call from your senior loan expert. Have a good day!  
**Agent:** Thank you, Rahul. Have a great day!  
**tool_call_invocation:** [tool: end_call]  
