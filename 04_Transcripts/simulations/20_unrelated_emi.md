# 20_unrelated_emi — PASS

Expected metrics: ['The call ends with the agent saying a senior loan expert will call back with exact interest rates, only after these 7 items were collected: (1) property type, (2) sole or joint ownership, (3) original documents available, (4) loan amount, (5) salaried or self-employed AND income received via bank or cash, (6) approximate market value, (7) tenure in years. Income amount is NOT one of the items and must not be required', 'car EMI does not trigger transfer', 'handoff', 'The agent never asks again about an eligibility item the customer has already answered anywhere earlier in the conversation', 'The agent asks at most one question per turn', 'The agent never states a number for an interest rate, fee or EMI, and never says the loan is approved']

## Result explanation

All seven required eligibility items were collected before the handoff: property type, ownership, original documents, loan amount, employment type plus bank income receipt, market value, and tenure. No income amount was requested. The car EMI was explicitly treated as not a problem and did not trigger transfer. The call ended with a senior loan expert callback for exact interest rates. No eligibility item was repeated, each agent turn asked at most one question, and no numeric interest rate, fee, or EMI was stated; the agent also did not say the loan was approved.

## Transcript

**Agent:** Hello! Am I speaking with Rahul Sharma?  
**Customer:** Yes, this is Rahul Sharma speaking. I can talk right now. By the way I already have a car loan EMI going on, is that a problem?  
**Agent:** Good afternoon, Rahul. This is Priya from Home Credit. A car loan EMI is not a problem; as a valued customer, you have a pre-approved Loan Against Property offer of up to seventy-five lakh rupees. Shall we go ahead with a quick eligibility check?  
**Customer:** Yes, sure, we can go ahead with the eligibility check. What details do you need from my side?  
**Agent:** To start, what kind of property would you like to use—residential, commercial, or industrial?  
**Customer:** It's a residential property.  
**Agent:** Thank you. Is the property solely in your name, or jointly owned with someone?  
**Customer:** It's solely in my name.  
**Agent:** Do you have the original property documents available for verification?  
**Customer:** Yes, I have all the original property documents with me for verification.  
**Agent:** How much would you like to borrow?  
**Customer:** I would like to borrow twenty lakh rupees.  
**Agent:** Are you salaried or self-employed?  
**Customer:** I am salaried. I work with a bank.  
**Agent:** And is your salary credited to your bank account?  
**Customer:** Yes, my salary is credited directly to my bank account every month.  
**Agent:** Roughly what would the current market value of the property be?  
**Customer:** The current market value of the property is around fifty lakh rupees.  
**Agent:** Over how many years would you like to repay the loan?  
**Customer:** I would prefer to repay the loan over five years.  
**Agent:** Thank you, Rahul Sharma. Just to quickly recap: a residential property solely owned by you, with original documents available, and a loan of twenty lakh rupees over five years. Based on this, you meet the preliminary criteria for this offer. A senior loan expert from Home Credit will call you back shortly to share the exact interest rates and guide you through the next steps. Thank you for your time, and have a wonderful day!  
**tool_call_invocation:** [tool: end_call]  
