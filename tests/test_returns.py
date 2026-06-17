import pytest
from datetime import datetime, timedelta
from src.models.user import User, UserRole
from src.models.book import Book
from src.models.author import Author
from src.models.loan import Loan, LoanStatus
from src.auth import create_access_token

@pytest.fixture
def student_token(db):
    user = User(
        username="student1",
        email="student1@example.com",
        hashed_password="hashed",
        role=UserRole.STUDENT
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return create_access_token(data={"sub": user.username}), user

@pytest.fixture
def librarian_token(db):
    user = User(
        username="librarian1",
        email="librarian1@example.com",
        hashed_password="hashed",
        role=UserRole.LIBRARIAN
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return create_access_token(data={"sub": user.username}), user

@pytest.fixture
def test_book(db):
    author = Author(name="Test Author")
    db.add(author)
    db.commit()
    db.refresh(author)
    
    book = Book(
        title="Test Book",
        author_id=author.id,
        isbn="1234567890",
        total_copies=5,
        available_copies=4 # One already out
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def test_return_book_success(client, db, librarian_token, student_token, test_book):
    lib_token, lib_user = librarian_token
    stu_token, stu_user = student_token
    
    # Create an active loan
    loan = Loan(
        user_id=stu_user.id,
        book_id=test_book.id,
        status=LoanStatus.ACTIVE,
        due_date=datetime.utcnow() + timedelta(days=7)
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    
    response = client.post(
        f"/api/loans/{loan.id}/return",
        json={"condition": "Good"},
        headers={"Authorization": f"Bearer {lib_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RETURNED"
    assert data["condition"] == "Good"
    assert data["total_fine"] == 0.0
    
    # Check book availability
    db.refresh(test_book)
    assert test_book.available_copies == 5

def test_return_book_overdue(client, db, librarian_token, student_token, test_book):
    lib_token, lib_user = librarian_token
    stu_token, stu_user = student_token
    
    # Create an overdue loan (10 days late)
    loan = Loan(
        user_id=stu_user.id,
        book_id=test_book.id,
        status=LoanStatus.ACTIVE,
        due_date=datetime.utcnow() - timedelta(days=10)
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    
    response = client.post(
        f"/api/loans/{loan.id}/return",
        json={"condition": "Damaged"},
        headers={"Authorization": f"Bearer {lib_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RETURNED"
    assert data["total_fine"] == 5.0 # 10 days * 0.50

def test_return_book_unauthorized(client, db, student_token, test_book):
    stu_token, stu_user = student_token
    
    loan = Loan(
        user_id=stu_user.id,
        book_id=test_book.id,
        status=LoanStatus.ACTIVE
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    
    # Student cannot return book
    response = client.post(
        f"/api/loans/{loan.id}/return",
        json={"condition": "Good"},
        headers={"Authorization": f"Bearer {stu_token}"}
    )
    assert response.status_code == 403

def test_get_my_loans(client, db, student_token, test_book):
    stu_token, stu_user = student_token
    
    loan = Loan(
        user_id=stu_user.id,
        book_id=test_book.id,
        status=LoanStatus.ACTIVE
    )
    db.add(loan)
    db.commit()
    
    response = client.get(
        "/api/loans/me",
        headers={"Authorization": f"Bearer {stu_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == stu_user.id

def test_get_active_and_overdue_loans(client, db, librarian_token, student_token, test_book):
    lib_token, lib_user = librarian_token
    stu_token, stu_user = student_token
    
    # Active loan
    loan1 = Loan(user_id=stu_user.id, book_id=test_book.id, status=LoanStatus.ACTIVE, due_date=datetime.utcnow() + timedelta(days=7))
    # Overdue loan
    loan2 = Loan(user_id=stu_user.id, book_id=test_book.id, status=LoanStatus.ACTIVE, due_date=datetime.utcnow() - timedelta(days=1))
    db.add(loan1)
    db.add(loan2)
    db.commit()
    
    # Active
    response = client.get("/api/loans/active", headers={"Authorization": f"Bearer {lib_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Overdue
    response = client.get("/api/loans/overdue", headers={"Authorization": f"Bearer {lib_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == loan2.id
