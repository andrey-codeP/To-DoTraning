from pydantic import BaseModel, Field, ConfigDict


class SUser(BaseModel):
    username: str = Field(..., min_length=4, max_length=15)


class SUserCreate(SUser):
    password: str = Field(..., min_length=6, max_length=20)


class SUserResponse(SUser):
    id: int
    is_active: bool = Field(default=True)

    model_config = ConfigDict(from_attributes=True)


#
