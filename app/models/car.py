from datetime import datetime

from sqlmodel import Field, SQLModel, text


class Car(SQLModel, table=True):
    __tablename__: str = "car"
    id: int | None = Field(default=None, primary_key=True)  # 车辆id
    car_number: str  # 车牌号,not null
    status: int = Field(default=0)  # 车辆状态0:未使用,1:使用中
    current_user_id: int | None = Field(default=None)  # 当前使用者id
    is_deleted: int = Field(default=0)  # 逻辑删除标识(0未删除,1已删除)
    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },  # 使用数据库端的当前时间
    )  # 更新时间
