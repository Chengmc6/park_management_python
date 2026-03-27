from pydantic import BaseModel, Field, field_validator


class CarAddRequestDto(BaseModel):
    car_number: str = Field(..., min_length=1, description="请输入车牌号")

    @field_validator("car_number")
    @classmethod
    def validate_number(cls, n: str):
        cleaned = n.strip()
        if not cleaned:
            raise ValueError("请输入非空字符")
        return cleaned
