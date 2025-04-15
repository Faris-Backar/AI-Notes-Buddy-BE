from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    uid: str
    email: EmailStr
    displayName: str
    photoURL: Optional[str] = None

class UserResponse(BaseModel):
    uid: str
    email: EmailStr
    displayName: str
    photoURL: Optional[str] = None
    createdDate: datetime
    modifiedDate: datetime 