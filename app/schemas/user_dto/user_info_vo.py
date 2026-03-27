from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserInfoVo(BaseModel):
    id: int | None = Field(None, description="用户id")
    username: str | None = Field(None, description="用户名")
    created_at: datetime | None = Field(None, description="创建时间")

    # 🔑 核心配置：允许从类属性初始化  # noqa: RUF003
    model_config = ConfigDict(from_attributes=True)
