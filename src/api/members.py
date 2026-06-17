from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.auth import require_role
from src.models.user import User, UserRole
from src.schemas.user import MemberResponse

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/", response_model=List[MemberResponse])
def list_members(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.LIBRARIAN)),
):
    return db.query(User).filter(User.role == UserRole.STUDENT).all()
