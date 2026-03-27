from pydantic import BaseModel, Field


class CarDeleteRequestDto(BaseModel):
    ids: list[int] = Field(default=[], description="车辆id")
