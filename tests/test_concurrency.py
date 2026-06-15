import pytest
import os
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from src.main import app
from src.models.user import User, UserRole
from src.models.book import Book
from src.models.author import Author
from src.models.loan_request import LoanRequest, LoanRequestStatus
from src.models.loan import Loan
from src.auth import create_access_token
from src.database import get_db, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# We use a separate engine for concurrency tests to avoid interference with other tests
# and to ensure we are testing real transaction isolation if possible.
# Use a file-based SQLite database for concurrency tests to ensure proper locking behavior.
DB_PATH = "test_concurrency.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def conc_db():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            pass
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    engine.dispose() # Dispose engine to close all connections
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            pass

def test_concurrent_approvals(conc_db):
    # Override get_db for the app to use our conc_db engine but create fresh sessions
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    # Setup: Create a librarian
    librarian = User(username="admin", email="admin@example.com", hashed_password="hashed", role=UserRole.LIBRARIAN)
    conc_db.add(librarian)
    
    # Setup: Create an author and a book with 1 copy
    author = Author(name="Author")
    conc_db.add(author)
    conc_db.commit()
    
    book = Book(title="Limited Book", author_id=author.id, isbn="CONC123", total_copies=1, available_copies=1)
    conc_db.add(book)
    conc_db.commit()

    # Setup: Create 3 students and 3 pending requests for the same book
    requests = []
    for i in range(3):
        student = User(username=f"student{i}", email=f"s{i}@example.com", hashed_password="hashed", role=UserRole.STUDENT)
        conc_db.add(student)
        conc_db.commit()
        
        req = LoanRequest(user_id=student.id, book_id=book.id, status=LoanRequestStatus.PENDING)
        conc_db.add(req)
        conc_db.commit()
        requests.append(req)

    token = create_access_token(data={"sub": librarian.username})
    headers = {"Authorization": f"Bearer {token}"}

    def approve_request(request_id):
        # Fresh request to the API
        return client.post(f"/api/loans/requests/{request_id}/approve", headers=headers)

    # Action: Simultaneously approve all 3 requests
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(approve_request, [r.id for r in requests]))

    # Assertion:
    # 1. Exactly one should succeed (200 OK)
    # 2. Others should fail (400 Bad Request because available_copies becomes 0)
    success_count = sum(1 for r in results if r.status_code == 200)
    failure_count = sum(1 for r in results if r.status_code == 400)

    # In SQLite, "FOR UPDATE" is ignored, so we might actually have a race condition 
    # if it weren't for SQLite's global write lock. 
    # SQLite only allows one writer at a time, so it naturally serializes these.
    assert success_count == 1
    assert failure_count == 2

    # Verify database state
    conc_db.refresh(book)
    assert book.available_copies == 0
    
    loans_count = conc_db.query(Loan).filter(Loan.book_id == book.id).count()
    assert loans_count == 1

    approved_requests_count = conc_db.query(LoanRequest).filter(
        LoanRequest.book_id == book.id,
        LoanRequest.status == LoanRequestStatus.APPROVED
    ).count()
    assert approved_requests_count == 1
    
    app.dependency_overrides.clear()
