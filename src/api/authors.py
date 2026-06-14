from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.author import Author
from src.models.user import UserRole
from src.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from src.auth import require_role

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(
    author: AuthorCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_role(UserRole.LIBRARIAN))
):
    db_author = Author(name=author.name, biography=author.biography)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.get("/", response_model=List[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(
    author_id: int, 
    author_update: AuthorUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_role(UserRole.LIBRARIAN))
):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    update_data = author_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_author, key, value)
    
    db.commit()
    db.refresh(db_author)
    return db_author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(
    author_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(require_role(UserRole.LIBRARIAN))
):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(db_author)
    db.commit()
    return None
