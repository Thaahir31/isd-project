from pydantic import BaseModel, ConfigDict
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    biography: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None

class AuthorResponse(AuthorBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
