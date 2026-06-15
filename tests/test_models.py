import pytest
from datetime import datetime, timedelta
from src.models.loan import Loan, LoanStatus

def test_loan_model_creation(db):
    # Setup
    from src.models.user import User
    from src.models.book import Book
    from src.models.author import Author

    author = Author(name="Test Author")
    db.add(author)
    db.commit()

    book = Book(title="Test Book", author_id=author.id, isbn="1234567890", total_copies=5, available_copies=5)
    db.add(book)
    db.commit()

    user = User(username="testuser", email="test@example.com", hashed_password="hashedpassword")
    db.add(user)
    db.commit()

    # Action
    loan = Loan(
        user_id=user.id,
        book_id=book.id,
        status=LoanStatus.ACTIVE,
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    db.add(loan)
    db.commit()

    # Assertion
    assert loan.id is not None
    assert loan.user_id == user.id
    assert loan.book_id == book.id
    assert loan.status == LoanStatus.ACTIVE
    assert loan.total_fine == 0.0
    assert loan.due_date > datetime.utcnow()
