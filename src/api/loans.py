from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from src.database import get_db
from src.auth import get_current_user, require_role
from src.models.user import User, UserRole
from src.models.book import Book
from src.models.loan_request import LoanRequest, LoanRequestStatus
from src.models.loan import Loan, LoanStatus
from src.schemas.loan_request import LoanRequestCreate, LoanRequestResponse
from src.schemas.loan import LoanResponse, LoanReturn
from src.logic.fines import calculate_overdue_fine

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
    
    # Check borrowing limit (max 3 active items: PENDING/APPROVED requests + ACTIVE loans)
    active_requests_count = db.query(LoanRequest).filter(
        LoanRequest.user_id == current_user.id,
        LoanRequest.status.in_([LoanRequestStatus.PENDING, LoanRequestStatus.APPROVED])
    ).count()
    
    active_loans_count = db.query(Loan).filter(
        Loan.user_id == current_user.id,
        Loan.status == LoanStatus.ACTIVE
    ).count()
    
    if (active_requests_count + active_loans_count) >= 3:
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

@router.post("/requests/{request_id}/approve", response_model=LoanResponse)
def approve_loan_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.LIBRARIAN))
):
    # 2. Fetch the LoanRequest by ID
    loan_request = db.query(LoanRequest).filter(LoanRequest.id == request_id).first()
    if not loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found")
    
    if loan_request.status != LoanRequestStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Cannot approve request in {loan_request.status} status")

    # 3. Fetch the Book record using SELECT FOR UPDATE
    # This locks the row on supported databases (Postgres/MySQL)
    book = db.query(Book).filter(Book.id == loan_request.book_id).with_for_update().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 4. Validate Book available_copies > 0
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available for this book")

    # Re-enforce the 3-active-items limit (loans + pending/approved requests)
    # The current request being approved is already in the count.
    active_requests_count = db.query(LoanRequest).filter(
        LoanRequest.user_id == loan_request.user_id,
        LoanRequest.status.in_([LoanRequestStatus.PENDING, LoanRequestStatus.APPROVED])
    ).count()
    
    active_loans_count = db.query(Loan).filter(
        Loan.user_id == loan_request.user_id,
        Loan.status == LoanStatus.ACTIVE
    ).count()
    
    if (active_requests_count + active_loans_count) > 3:
        raise HTTPException(
            status_code=400,
            detail="User has reached maximum borrowing limit"
        )

    # 5. Action:
    # Use an atomic update to be extra safe and handle SQLite concurrency tests correctly
    updated_rows = db.query(Book).filter(
        Book.id == loan_request.book_id,
        Book.available_copies > 0
    ).update(
        {"available_copies": Book.available_copies - 1},
        synchronize_session=False
    )
    
    if updated_rows == 0:
        # This could happen if another process snatched the last copy between our check and update
        raise HTTPException(status_code=400, detail="No copies available for this book")

    loan_request.status = LoanRequestStatus.APPROVED
    
    new_loan = Loan(
        user_id=loan_request.user_id,
        book_id=loan_request.book_id,
        status=LoanStatus.ACTIVE,
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    db.add(new_loan)
    
    # 6. Commit transaction
    db.commit()
    db.refresh(new_loan)
    return new_loan

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

@router.post("/{loan_id}/return", response_model=LoanResponse)
def return_book(
    loan_id: int,
    return_data: LoanReturn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.LIBRARIAN))
):
    # 1. Fetch Loan by ID (ensure status is ACTIVE)
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    
    if loan.status != LoanStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Cannot return loan with status {loan.status}"
        )

    # 2. Calculate fine
    now = datetime.utcnow()
    fine = calculate_overdue_fine(loan.due_date, now)

    # 3. Update Loan
    loan.status = LoanStatus.RETURNED
    loan.returned_at = now
    loan.condition = return_data.condition
    loan.total_fine = fine

    # 4. Fetch Book and increment available_copies
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if book:
        book.available_copies += 1
    
    db.commit()
    db.refresh(loan)
    return loan

@router.get("/me", response_model=List[LoanResponse])
def get_my_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STUDENT))
):
    """
    Returns list of loans belonging to the authenticated student.
    """
    return db.query(Loan).filter(Loan.user_id == current_user.id).all()

@router.get("/active", response_model=List[LoanResponse])
def get_active_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.LIBRARIAN))
):
    """
    Returns all currently ACTIVE loans.
    """
    return db.query(Loan).filter(Loan.status == LoanStatus.ACTIVE).all()

@router.get("/overdue", response_model=List[LoanResponse])
def get_overdue_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.LIBRARIAN))
):
    """
    Returns loans where due_date < now and status is ACTIVE.
    """
    now = datetime.utcnow()
    return db.query(Loan).filter(
        Loan.status == LoanStatus.ACTIVE,
        Loan.due_date < now
    ).all()
