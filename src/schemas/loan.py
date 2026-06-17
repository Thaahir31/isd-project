from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.models.loan import LoanStatus

class LoanBase(BaseModel):
    user_id: int
    book_id: int
    status: LoanStatus

class LoanReturn(BaseModel):
    condition: str  # Good, Damaged, Lost

class LoanResponse(LoanBase):
    id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime] = None
    condition: Optional[str] = None
    total_fine: float

    class Config:
        from_attributes = True
