from datetime import datetime

from pydantic import BaseModel, Field


class CarRideRequestDto(BaseModel):
    car_id: int = Field(..., description="请输入车辆id")
    user_id: int = Field(..., description="请输入使用者id")
    ride_time: datetime = Field(..., description="开始乘坐时间")
    ride_alcohol_level: float = Field(default=0, description="乘坐时的酒精度数")


class CarDropRequestDto(BaseModel):
    car_id: int = Field(..., description="请输入车辆id")
    user_id: int = Field(..., description="请输入使用者id")
    drop_time: datetime = Field(..., description="下车时间")
    drop_alcohol_level: float = Field(default=0, description="下车时的酒精度数")
