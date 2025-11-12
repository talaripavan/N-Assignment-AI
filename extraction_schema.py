from pydantic import BaseModel
from typing import Optional , Literal

class DocumentExtraction(BaseModel):
    """Flat extraction result with all possible fields as Optional."""
    
    # Document type identifier
    document_type: Literal["bank_statement", "salary_slip", "itr", "utility_bill", "check"]
    
    # Bank Statement fields
    account_holder_name: Optional[str] = None
    account_number: Optional[str] = None
    statement_period_start: Optional[str] = None
    statement_period_end: Optional[str] = None
    opening_balance: Optional[float] = None
    closing_balance: Optional[float] = None
    
    # Salary Slip fields
    employee_name: Optional[str] = None
    employee_id: Optional[str] = None
    month: Optional[str] = None
    year: Optional[str] = None
    basic_salary: Optional[float] = None
    allowances: Optional[float] = None
    deductions: Optional[float] = None
    net_salary: Optional[float] = None
    employer_name: Optional[str] = None
    
    # ITR fields
    taxpayer_name: Optional[str] = None
    pan_number: Optional[str] = None
    assessment_year: Optional[str] = None
    total_income: Optional[float] = None
    tax_payable: Optional[float] = None
    filing_date: Optional[str] = None
    
    # Utility Bill fields
    consumer_name: Optional[str] = None
    consumer_number: Optional[str] = None
    bill_date: Optional[str] = None
    due_date: Optional[str] = None
    billing_period_start: Optional[str] = None
    billing_period_end: Optional[str] = None
    total_amount: Optional[float] = None
    utility_type: Optional[str] = None
    
    # Check fields
    check_number: Optional[str] = None
    payee_name: Optional[str] = None
    amount_in_numbers: Optional[float] = None
    amount_in_words: Optional[str] = None
    bank_name: Optional[str] = None