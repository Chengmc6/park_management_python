import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.common.api_response import ApiResponse
from app.common.result_code import ResultCode
from app.exception.business_exception import BusinessException

logger = logging.getLogger(__name__)


def exception_handler(app: FastAPI):
    """
    注册全局异常处理器,确保所有接口返回统一的 ApiResponse 格式
    """

    @app.exception_handler(BusinessException)
    async def business_exception(request: Request, exception: BusinessException):

        result = ResultCode.get_by_code(exception.code)

        return JSONResponse(
            status_code=200,
            content=ApiResponse.fail(
                result=result,
                message=exception.message,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request, exception: ValidationError
    ):
        if isinstance(exception, (RequestValidationError, ValidationError)):
            errors = exception.errors()
            msg = (
                f"{errors[0]['loc'][-1]}: {errors[0]['msg']}"
                if errors
                else "参数校验失败"
            )
        else:
            msg = "数据格式解析错误"
        return JSONResponse(
            status_code=200,
            content=ApiResponse.fail(
                result=ResultCode.VALIDATION_ERROR, message=msg
            ).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handle(request: Request, exception: HTTPException):
        return JSONResponse(
            status_code=exception.status_code,
            content=ApiResponse.fail(
                result=exception.status_code, message=exception.detail
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exception: Exception):
        # 非常重要:在控制台/日志文件中打印真正的错误堆栈
        logger.error(f"全局异常捕捉: {exception!s}", exc_info=True)
        return JSONResponse(
            status_code=200,
            content=ApiResponse.fail(
                result=ResultCode.UNKNOWN_ERROR, message="服务器内部错误,请稍后重试"
            ).model_dump(),
        )
