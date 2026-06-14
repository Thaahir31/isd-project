import pytest
from src.models.user import User, UserRole
from src.auth import get_password_hash
from src.models.author import Author

@pytest.fixture
def auth_headers(client, db):
    # Create librarian
    librarian = User(
        username="admin", 
        email="admin@test.com", 
        hashed_password=get_password_hash("adminpass"), 
        role=UserRole.LIBRARIAN
    )
    # Create student
    student = User(
        username="student", 
        email="student@test.com", 
        hashed_password=get_password_hash("studentpass"), 
        role=UserRole.STUDENT
    )
    db.add(librarian)
    db.add(student)
    db.commit()

    def _get_headers(username, password):
        response = client.post("/auth/login", data={"username": username, "password": password})
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return {
        "librarian": _get_headers("admin", "adminpass"),
        "student": _get_headers("student", "studentpass")
    }

def test_create_author_as_librarian(client, auth_headers):
    response = client.post(
        "/authors/",
        json={"name": "J.K. Rowling", "biography": "Author of Harry Potter"},
        headers=auth_headers["librarian"]
    )
    assert response.status_code == 201
    assert response.json()["name"] == "J.K. Rowling"

def test_create_author_as_student_fails(client, auth_headers):
    response = client.post(
        "/authors/",
        json={"name": "J.R.R. Tolkien"},
        headers=auth_headers["student"]
    )
    assert response.status_code == 403

def test_get_authors(client, db):
    # Add an author directly
    author = Author(name="Isaac Asimov")
    db.add(author)
    db.commit()

    response = client.get("/authors/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert any(a["name"] == "Isaac Asimov" for a in response.json())

def test_update_author_as_librarian(client, db, auth_headers):
    author = Author(name="Unknown Author")
    db.add(author)
    db.commit()

    response = client.put(
        f"/authors/{author.id}",
        json={"name": "Known Author"},
        headers=auth_headers["librarian"]
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Known Author"

def test_delete_author_as_librarian(client, db, auth_headers):
    author = Author(name="To Be Deleted")
    db.add(author)
    db.commit()

    response = client.delete(
        f"/authors/{author.id}",
        headers=auth_headers["librarian"]
    )
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/authors/{author.id}")
    assert response.status_code == 404
