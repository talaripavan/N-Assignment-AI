"""
Configuration file for document classification system.
Contains keywords, prompts, and constants.
"""

PYDANTIC_CLASSIFICATION_PROMPT = """
You are an intelligent financial document classifier. 
Your task is to carefully analyze the given text and determine which of the following document categories it belongs to. 
Base your decision only on the document's content, structure, and terminology — not assumptions.

If the content is too limited, unclear, or unrelated, classify it as "unknown" instead of guessing.

Possible categories:

1. Bank Statement — 
   Bank account statements that show transaction histories, balances, or summaries over a period of time. 
   Common indicators: account number, transaction table, debit/credit columns, running balance, date range.
   Negative indicators: single payment instruction, payee name, or signature (those indicate a check).

2. Salary Slip — 
   Employee payslips or payroll documents showing employee name, gross/net salary, deductions, and allowances.
   Common indicators: "Employee ID", "Basic Pay", "Gross Salary", "Net Pay", "Deductions".
   Negative indicators: list of account transactions or “Pay to the order of”.

3. ITR_Form 16 — 
   Income Tax Return or related tax filing forms. 
   Common indicators: “Assessment Year”, “PAN”, “Total Income”, “Tax Payable”, “Refund”, “Acknowledgement Number”.
   Negative indicators: account transactions or salary breakup.

4. Utility — 
   Bills for electricity, water, gas, phone, or internet showing usage, charges, and payment due date. 
   Common indicators: “Bill Number”, “Units Consumed”, “Amount Due”, “Billing Period”, “Consumer ID”.

5. Check — 
   A single payment instrument (cheque) containing payer, payee, amount (in words and numbers), date, and signature. 
   Common indicators: “Pay to the order of”, amount written in words, signature line, “Account Payee Only”, bank name.
   Negative indicators: multiple transactions or balance summaries (those indicate bank statements).

6. unknown — 
   If there is not enough context or distinctive features to confidently classify the document, 
   select this category. Do not hallucinate or guess.

---

Before deciding, consider:
- Does the document have enough identifiable content?
- Are there clear indicators that match one category strongly?
- If not, use "unknown" with a low confidence (< 0.5).

---

Analyze the text below carefully and output the result in the following structured json format:

"document_type": "<one of the 6 types>",
"confidence": <float between 0.0 and 1.0>,
"reasoning": "<explain why you classified it this way>",
"key_indicators": [<list of key indicators found>],
"negative_indicators": [<list of features that ruled out other document types>],

Document content:
{context_str}
"""


# API Configuration
API_CONFIG = {
    "model": "gpt-4o-mini",
    "temperature": 0.2,
    "max_tokens": 1000
}