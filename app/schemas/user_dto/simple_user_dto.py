from pydantic import BaseModel, Field


class SimpleUserDto(BaseModel):
    user_id: int | None = Field(None, description="用户id")
    username: str | None = Field(None, description="用户名")
