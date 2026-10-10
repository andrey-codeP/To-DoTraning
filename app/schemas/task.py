from pydantic import BaseModel, Field
from datetime import datetime

class Task(BaseModel):
    title: str = Field(default="some task", max_length=100)
    description:str = Field(max_length=500)
    created_at: datetime
    completed_at: datetime
    completed: bool

