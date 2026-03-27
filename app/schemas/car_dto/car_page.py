from pydantic import BaseModel, ConfigDict, Field


class CarPageResponseVo(BaseModel):
    id: int | None = Field(default=None, description="车辆id")
    car_number: str | None = Field(default=None, description="车牌号")
    status: int | None = Field(default=None, description="车辆状态")
    current_user: int | None = Field(default=None, description="当前使用者id")

    model_config = ConfigDict(from_attributes=True)
