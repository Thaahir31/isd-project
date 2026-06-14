from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.book import Book
from src.models.author import Author
from src.models.user import UserRole
from src.schemas.book import BookCreate, BookUpdate, BookResponse
from src.auth import require_role

from sqlalchemy import or_

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/search", response_model=List[BookResponse])
def search_books(
    q: str, 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """
    Search books by title, author name, or ISBN.
    Uses ILIKE for fuzzy matching on title and author.
    """
    query = db.query(Book).join(Author)
    
    # Simple fuzzy search using ILIKE
    search_filter = or_(
        Book.title.ilike(f"%{q}%"),
        Author.name.ilike(f"%{q}%"),
        Book.isbn == q.replace("-", "").replace(" ", "") # Exact match for normalized ISBN
    )
    
    results = query.filter(search_filter).offset(skip).limit(limit).all()
    return results

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_role(UserRole.LIBRARIAN))
):
    # Verify author exists
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=400, detail="Author not found")
    
    # Check if ISBN already exists
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    db_book = Book(
        title=book.title,
        author_id=book.author_id,
        isbn=book.isbn,
        total_copies=book.total_copies,
        available_copies=book.total_copies, # D-F-004: defaults to total_copies
        category=book.category
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int, 
    book_update: BookUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_role(UserRole.LIBRARIAN))
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book_update.author_id:
        author = db.query(Author).filter(Author.id == book_update.author_id).first()
        if not author:
            raise HTTPException(status_code=400, detail="Author not found")

    update_data = book_update.model_dump(exclude_unset=True)
    
    # If total_copies is updated, we might need to adjust available_copies
    # For now, let's keep it simple: if total_copies increases, available_copies increases by same amount
    if "total_copies" in update_data:
        diff = update_data["total_copies"] - db_book.total_copies
        db_book.available_copies += diff
        if db_book.available_copies < 0:
            db_book.available_copies = 0

    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(require_role(UserRole.LIBRARIAN))
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return None
