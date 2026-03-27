from pydantic import BaseModel, Field


class UserLoginResponseVo(BaseModel):
    id: int | None = Field(None, description="用户id")
    username: str | None = Field(None, description="用户名")
    token: str | None = Field(None, description="用户token")
