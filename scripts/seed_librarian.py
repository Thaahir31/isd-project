import sys
import os

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import SessionLocal
from src.models.user import User, UserRole
from src.auth import get_password_hash

def seed():
    db = SessionLocal()
    try:
        librarian = db.query(User).filter(User.username == "admin").first()
        if not librarian:
            print("Creating default librarian...")
            librarian = User(
                username="admin",
                email="admin@library.com",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.LIBRARIAN
            )
            db.add(librarian)
            db.commit()
            print("Librarian 'admin' created successfully.")
        else:
            print("Librarian 'admin' already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
