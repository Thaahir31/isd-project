from src.models.user import User, UserRole
from src.auth import get_password_hash

def test_login_success(client, db):
    # Setup: Create a test user
    hashed_password = get_password_hash("testpassword")
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_password,
        role=UserRole.STUDENT
    )
    db.add(user)
    db.commit()

    # Test: Login
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(client, db):
    # Test: Login with wrong password
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "wrongpassword"}
    )
    assert response.status_code == 401
