# Models
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    content: str
    createUserName: str
    isActive: bool = True
    status: str = "active"

class NoteCreate(NoteBase):
    userUid: str

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    isActive: Optional[bool] = None
    status: Optional[str] = None

class NoteResponse(NoteBase):
    id: str
    userUid: str
    createdDate: datetime
    modifiedDate: datetime
