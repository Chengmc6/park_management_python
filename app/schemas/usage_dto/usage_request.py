from pydantic import BaseModel, Field


class UsageRequestDto(BaseModel):
    car_id: int = Field(..., description="请输入车辆id")
    page_num: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=10, description="每页展示条数")
