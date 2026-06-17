from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Float, String
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timedelta
from src.database import Base

class LoanStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14), nullable=False)
    returned_at = Column(DateTime, nullable=True)
    condition = Column(String, nullable=True)
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE, nullable=False)
    total_fine = Column(Float, default=0.0, nullable=False)

    user = relationship("User")
    book = relationship("Book")
