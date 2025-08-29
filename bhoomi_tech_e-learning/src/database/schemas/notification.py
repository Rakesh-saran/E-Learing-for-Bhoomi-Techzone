from pydantic import BaseModel, Field
from typing import Optional

class NotificationSchema(BaseModel):
    id: Optional[str]
    user_id: str = Field(...)
    message: str = Field(...)
    is_read: bool = False
