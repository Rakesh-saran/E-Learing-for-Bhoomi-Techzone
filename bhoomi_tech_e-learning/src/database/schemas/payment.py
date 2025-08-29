from pydantic import BaseModel, Field
from typing import Optional

class PaymentSchema(BaseModel):
    id: Optional[str]
    user_id: str = Field(...)
    course_id: str = Field(...)
    amount: float = Field(...)
    status: str = Field(...)
