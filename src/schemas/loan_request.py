from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.models.loan_request import LoanRequestStatus

class LoanRequestBase(BaseModel):
    book_id: int

class LoanRequestCreate(LoanRequestBase):
    pass

class LoanRequestResponse(LoanRequestBase):
    id: int
    user_id: int
    status: LoanRequestStatus
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True
