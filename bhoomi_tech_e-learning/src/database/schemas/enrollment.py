from pydantic import BaseModel, Field
from typing import Optional

class EnrollmentSchema(BaseModel):
    id: Optional[str]
    user_id: str = Field(...)
    course_id: str = Field(...)
    progress: float = 0.0
