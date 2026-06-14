from src.auth import create_access_token
from src.models.user import UserRole, User
from src.auth import get_password_hash
import pytest

@pytest.fixture
def test_users(db):
    # Create a librarian
    librarian = User(
        username="lib", email="lib@test.com", 
        hashed_password=get_password_hash("pass"), role=UserRole.LIBRARIAN
    )
    # Create a student
    student = User(
        username="stu", email="stu@test.com", 
        hashed_password=get_password_hash("pass"), role=UserRole.STUDENT
    )
    db.add(librarian)
    db.add(student)
    db.commit()
    return librarian, student

def test_librarian_can_access_restricted_route(client, test_users):
    # Login as librarian
    response = client.post("/auth/login", data={"username": "lib", "password": "pass"})
    token = response.json()["access_token"]
    
    response = client.get("/librarian-only", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Hello Librarian"

def test_student_cannot_access_restricted_route(client, test_users):
    # Login as student
    response = client.post("/auth/login", data={"username": "stu", "password": "pass"})
    token = response.json()["access_token"]
    
    response = client.get("/librarian-only", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Operation not permitted"
