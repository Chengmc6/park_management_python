from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageResult(BaseModel, Generic[T]):
    total: int = Field(default=0, description="数据总条数")
    page_num: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=10, description="每页数据条数")
    total_pages: int = Field(default=0, description="总页数")
    records: list[T] = Field(default=[], description="展示数据")
