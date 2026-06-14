from sqlalchemy import Column, Integer, String, Enum
import enum
from src.database import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    LIBRARIAN = "librarian"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
