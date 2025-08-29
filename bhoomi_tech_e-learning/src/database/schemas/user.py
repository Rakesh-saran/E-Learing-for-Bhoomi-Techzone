from pydantic import BaseModel, Field
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[str]
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    role: str = Field(...)
    is_active: bool = True
    avatar: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = None
