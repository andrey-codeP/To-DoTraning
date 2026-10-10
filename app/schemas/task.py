from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(default="some task", max_length=100)
    description: str = Field(max_length=500)


class TaskResponse(TaskCreate):
    id: int
    created_at: datetime
    completed_at: datetime
    completed: bool

    model_config = ConfigDict(from_attributes=True)
