from datetime import datetime

from sqlmodel import Field, SQLModel


class CarUsage(SQLModel, table=True):
    __tablename__: str = "car_usage"

    id: int | None = Field(default=None, primary_key=True)  # 使用履历id
    car_id: int  # 车辆id,not null
    user_id: int  # 使用者id,not null
    ride_time: datetime = Field(default_factory=datetime.now)  # 乘车时间,not null
    ride_alcohol_level: float  # 乘车时的酒精度数
    drop_time: datetime | None = Field(default=None)  # 下车时间
    drop_alcohol_level: float | None = Field(default=None)  # 下车时的酒精度数
