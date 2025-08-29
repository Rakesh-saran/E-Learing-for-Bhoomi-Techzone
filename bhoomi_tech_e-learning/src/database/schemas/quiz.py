from pydantic import BaseModel, Field
from typing import Optional, List

class QuestionSchema(BaseModel):
    question: str
    options: List[str]
    answer: str

class QuizSchema(BaseModel):
    id: Optional[str]
    course_id: str = Field(...)
    lesson_id: Optional[str] = None
    questions: List[QuestionSchema] = []
