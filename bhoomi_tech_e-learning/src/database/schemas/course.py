from pydantic import BaseModel, Field
from typing import Optional, List

class CourseResponse(BaseModel):
    id: Optional[str]
    title: str = Field(...)
    description: str = Field(...)
    instructor_id: str = Field(...)
    lessons: List[str] = []
    price: Optional[float] = None
    is_active: bool = True
    
class CourseCreate(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    lessons: List[str] = []
    price: Optional[float] = None
    is_active: bool = True

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    lessons: Optional[List[str]] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
