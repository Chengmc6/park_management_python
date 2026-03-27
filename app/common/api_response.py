from typing import Generic, Self, TypeVar

from pydantic import BaseModel, ConfigDict

from app.common.result_code import ResultCode

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    code: int
    message: str
    data: T | None = None

    @classmethod
    def success(cls, message: str | None = None, data: T | None = None) -> Self:
        msg = message if message else ResultCode.SUCCESS.message
        return cls(code=ResultCode.SUCCESS.code, message=msg, data=data)

    @classmethod
    def fail(cls, result: ResultCode | int, message: str | None = None) -> Self:
        if isinstance(result, ResultCode):
            status_code = result.code
            msg = message if message else result.message
        else:
            status_code = result
            msg = message if message is not None else "操作失败"
        return cls(code=status_code, message=msg, data=None)
