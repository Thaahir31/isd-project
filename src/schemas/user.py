from pydantic import BaseModel
from src.models.user import UserRole


class MemberResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True
