from pydantic import BaseModel
from typing import List

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: List[str]  # List of user's answers

class QuizResult(BaseModel):
    id: str = None
    user_id: str
    quiz_id: str
    score: float
    total_questions: int
    correct_answers: int
