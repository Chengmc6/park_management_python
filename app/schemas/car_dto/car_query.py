from pydantic import BaseModel, Field


class CarQueryRequestDto(BaseModel):
    car_number: str | None = Field(default=None, description="车牌号")
    page_num: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=10, description="每页数据量")

    @classmethod
    def validate_number(cls, n: str):
        cleaned = n.strip()
        if not cleaned:
            raise ValueError("请输入非空字符")
        return cleaned
