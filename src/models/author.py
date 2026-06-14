from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    biography = Column(Text, nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
