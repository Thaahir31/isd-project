import pytest
from src.models.user import User, UserRole
from src.auth import get_password_hash
from src.models.author import Author
from src.models.book import Book

@pytest.fixture
def auth_headers(client, db):
    # Create librarian
    librarian = User(
        username="admin_books", 
        email="admin_books@test.com", 
        hashed_password=get_password_hash("adminpass"), 
        role=UserRole.LIBRARIAN
    )
    db.add(librarian)
    db.commit()

    response = client.post("/auth/login", data={"username": "admin_books", "password": "adminpass"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_author(db):
    author = Author(name="Test Author")
    db.add(author)
    db.commit()
    return author

def test_create_book_as_librarian(client, auth_headers, test_author):
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author_id": test_author.id,
            "isbn": "978-3-16-148410-0",
            "total_copies": 5,
            "category": "Science"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["isbn"] == "9783161484100" # Normalized
    assert data["available_copies"] == 5

def test_create_book_invalid_isbn_fails(client, auth_headers, test_author):
    response = client.post(
        "/books/",
        json={
            "title": "Bad ISBN Book",
            "author_id": test_author.id,
            "isbn": "12345",
            "total_copies": 1
        },
        headers=auth_headers
    )
    assert response.status_code == 422 # Pydantic validation error

def test_create_book_duplicate_isbn_fails(client, auth_headers, test_author, db):
    # Setup: Create a book directly
    book = Book(title="Original", author_id=test_author.id, isbn="9783161484100")
    db.add(book)
    db.commit()

    response = client.post(
        "/books/",
        json={
            "title": "Duplicate",
            "author_id": test_author.id,
            "isbn": "978-3-16-148410-0",
            "total_copies": 1
        },
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_books(client, db, test_author):
    book = Book(title="Book 1", author_id=test_author.id, isbn="9783161484100")
    db.add(book)
    db.commit()

    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_update_book_copies(client, db, auth_headers, test_author):
    book = Book(title="Update Me", author_id=test_author.id, isbn="9783161484100", total_copies=2, available_copies=2)
    db.add(book)
    db.commit()

    response = client.put(
        f"/books/{book.id}",
        json={"total_copies": 10},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_copies"] == 10
    assert data["available_copies"] == 10 # 2 + (10 - 2)
