from pydantic import BaseModel, Field
from typing import Optional

class ReviewSchema(BaseModel):
    id: Optional[str]
    user_id: str = Field(...)
    course_id: str = Field(...)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
