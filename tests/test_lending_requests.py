import pytest
from fastapi.testclient import TestClient
from src.models.user import User, UserRole
from src.models.book import Book
from src.models.loan_request import LoanRequest, LoanRequestStatus
from src.auth import create_access_token
from datetime import datetime, timedelta

@pytest.fixture
def student_token(db):
    user = User(username="student1", email="student1@example.com", hashed_password="hashed_password", role=UserRole.STUDENT)
    db.add(user)
    db.commit()
    db.refresh(user)
    return create_access_token(data={"sub": user.username})

@pytest.fixture
def librarian_token(db):
    user = User(username="librarian1", email="librarian1@example.com", hashed_password="hashed_password", role=UserRole.LIBRARIAN)
    db.add(user)
    db.commit()
    db.refresh(user)
    return create_access_token(data={"sub": user.username})

@pytest.fixture
def sample_book(db):
    book = Book(title="Sample Book", author_id=1, isbn="1234567890", total_copies=5, available_copies=5)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def test_create_loan_request(client, student_token, sample_book):
    response = client.post(
        "/api/loans/requests",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"book_id": sample_book.id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["book_id"] == sample_book.id
    assert data["status"] == "PENDING"

def test_max_borrowing_limit(client, student_token, db):
    # Create a book
    book = Book(title="Another Book", author_id=1, isbn="0987654321", total_copies=5, available_copies=5)
    db.add(book)
    db.commit()
    
    # Create 3 pending requests
    for i in range(3):
        client.post(
            "/api/loans/requests",
            headers={"Authorization": f"Bearer {student_token}"},
            json={"book_id": book.id}
        )
        # Note: In my implementation I blocked duplicate pending requests for the same book, 
        # so I should probably use different books or my test is slightly off if it uses the same book.
        # Actually I'll use different books to be sure.
        book_i = Book(title=f"Book {i}", author_id=1, isbn=f"isbn-{i}", total_copies=5, available_copies=5)
        db.add(book_i)
        db.commit()
        client.post(
            "/api/loans/requests",
            headers={"Authorization": f"Bearer {student_token}"},
            json={"book_id": book_i.id}
        )

    # 4th request should fail
    book4 = Book(title="Book 4", author_id=1, isbn="isbn-4", total_copies=5, available_copies=5)
    db.add(book4)
    db.commit()
    response = client.post(
        "/api/loans/requests",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"book_id": book4.id}
    )
    assert response.status_code == 400
    assert "Maximum borrowing limit reached" in response.json()["detail"]

def test_list_requests_librarian(client, librarian_token, student_token, sample_book):
    # Create a request
    client.post(
        "/api/loans/requests",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"book_id": sample_book.id}
    )
    
    response = client.get(
        "/api/loans/requests",
        headers={"Authorization": f"Bearer {librarian_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_deny_request(client, librarian_token, student_token, sample_book, db):
    # Create a request
    resp = client.post(
        "/api/loans/requests",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"book_id": sample_book.id}
    )
    request_id = resp.json()["id"]
    
    response = client.post(
        f"/api/loans/requests/{request_id}/deny",
        headers={"Authorization": f"Bearer {librarian_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "DENIED"

def test_cleanup_expired_requests(client, librarian_token, student_token, sample_book, db):
    # Create a request
    resp = client.post(
        "/api/loans/requests",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"book_id": sample_book.id}
    )
    request_id = resp.json()["id"]
    
    # Manually expire it in the DB
    loan_request = db.query(LoanRequest).filter(LoanRequest.id == request_id).first()
    loan_request.expires_at = datetime.utcnow() - timedelta(days=1)
    db.commit()
    
    response = client.post(
        "/api/loans/requests/cleanup-expired",
        headers={"Authorization": f"Bearer {librarian_token}"}
    )
    assert response.status_code == 200
    assert "Cleaned up 1 expired requests" in response.json()["message"]
    
    db.refresh(loan_request)
    assert loan_request.status == LoanRequestStatus.EXPIRED
