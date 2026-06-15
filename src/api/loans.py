from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.database import get_db
from src.auth import get_current_user, require_role
from src.models.user import User, UserRole
from src.models.book import Book
from src.models.loan_request import LoanRequest, LoanRequestStatus
from src.schemas.loan_request import LoanRequestCreate, LoanRequestResponse

router = APIRouter(prefix="/api/loans", tags=["loans"])

@router.post("/requests", response_model=LoanRequestResponse, status_code=status.HTTP_201_CREATED)
def create_loan_request(
    request: LoanRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STUDENT))
):
    # Check if book exists
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check borrowing limit (max 3 active items: PENDING or APPROVED requests + ACTIVE loans)
    # TODO: Also check Loan model for ACTIVE/OVERDUE loans once Loan model is implemented
    active_requests_count = db.query(LoanRequest).filter(
        LoanRequest.user_id == current_user.id,
        LoanRequest.status.in_([LoanRequestStatus.PENDING, LoanRequestStatus.APPROVED])
    ).count()
    
    if active_requests_count >= 3:
        raise HTTPException(
            status_code=400,
            detail="Maximum borrowing limit reached (3 active requests/loans)"
        )
    
    # Check if user already has a PENDING request for this book
    existing_request = db.query(LoanRequest).filter(
        LoanRequest.user_id == current_user.id,
        LoanRequest.book_id == request.book_id,
        LoanRequest.status == LoanRequestStatus.PENDING
    ).first()
    
    if existing_request:
        raise HTTPException(status_code=400, detail="You already have a pending request for this book")

    new_request = LoanRequest(
        user_id=current_user.id,
        book_id=request.book_id,
        status=LoanRequestStatus.PENDING
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/requests", response_model=List[LoanRequestResponse])
def list_loan_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.LIBRARIAN))
):
    return db.query(LoanRequest).filter(LoanRequest.status == LoanRequestStatus.PENDING).all()

@router.post("/requests/{request_id}/deny", response_model=LoanRequestResponse)
def deny_loan_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.LIBRARIAN))
):
    loan_request = db.query(LoanRequest).filter(LoanRequest.id == request_id).first()
    if not loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found")
    
    if loan_request.status != LoanRequestStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Cannot deny request in {loan_request.status} status")
    
    loan_request.status = LoanRequestStatus.DENIED
    db.commit()
    db.refresh(loan_request)
    return loan_request

@router.post("/requests/cleanup-expired")
def cleanup_expired_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.LIBRARIAN))
):
    now = datetime.utcnow()
    
    expired_count = db.query(LoanRequest).filter(
        LoanRequest.status == LoanRequestStatus.PENDING,
        LoanRequest.expires_at < now
    ).update({LoanRequest.status: LoanRequestStatus.EXPIRED}, synchronize_session=False)
    
    db.commit()
    return {"message": f"Cleaned up {expired_count} expired requests"}
