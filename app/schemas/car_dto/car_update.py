from pydantic import BaseModel, ConfigDict, Field


class CarUpdateRequestDto(BaseModel):
    id: int = Field(..., description="请输入车辆id")
    car_number: str | None = Field(
        default=None, min_length=1, description="请输入非空字符"
    )
    status: int | None = Field(default=None, description="请选择车辆状态")

    @classmethod
    def validate_number(cls, n: str):
        cleaned = n.strip()
        if not cleaned:
            raise ValueError("请输入非空字符")
        return cleaned


class CarUpdateResponseVo(BaseModel):
    id: int | None = Field(default=None, description="车辆id")
    car_number: str | None = Field(default=None, min_length=1, description="车牌号")
    status: int | None = Field(default=None, description="车辆状态")

    model_config = ConfigDict(from_attributes=True)
