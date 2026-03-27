from datetime import datetime

from pydantic import BaseModel, Field


class UsageResponseVo(BaseModel):
    car_number: str | None = Field(default=None, description="车牌号")
    username: str | None = Field(default=None, description="使用者姓名")
    ride_time: datetime | None = Field(default=None)
    ride_alcohol_level: float = Field(default=0)
    drop_time: datetime | None = Field(default=None)
    drop_alcohol_level: float = Field(default=0)
