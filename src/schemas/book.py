from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from src.logic.isbn import validate_isbn13, normalize_isbn

class BookBase(BaseModel):
    title: str
    author_id: int
    isbn: str
    total_copies: Optional[int] = 1
    category: Optional[str] = None

    @field_validator("isbn")
    @classmethod
    def isbn_must_be_valid(cls, v: str) -> str:
        if not validate_isbn13(v):
            raise ValueError("Invalid ISBN-13 format")
        return normalize_isbn(v)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    isbn: Optional[str] = None
    total_copies: Optional[int] = None
    category: Optional[str] = None

    @field_validator("isbn")
    @classmethod
    def isbn_must_be_valid(cls, v: str) -> str:
        if v is not None:
            if not validate_isbn13(v):
                raise ValueError("Invalid ISBN-13 format")
            return normalize_isbn(v)
        return v

class BookResponse(BookBase):
    id: int
    available_copies: int
    
    model_config = ConfigDict(from_attributes=True)
