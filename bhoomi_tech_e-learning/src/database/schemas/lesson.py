from pydantic import BaseModel, Field
from typing import Optional

class LessonSchema(BaseModel):
    id: Optional[str]
    course_id: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    video_url: Optional[str] = None
    document_url: Optional[str] = None
