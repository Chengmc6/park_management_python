import uvicorn
from fastapi import APIRouter, Depends, FastAPI

from app.api.v1.dependencies import get_current_user
from app.api.v1.endpoints import auth, car_operate, usage
from app.core.config import settings
from app.exception.exception_handler import exception_handler

app = FastAPI(title=settings.app_name, debug=settings.debug)

# 注册全局异常处理器
exception_handler(app=app)

api_router = APIRouter()
api_router.include_router(auth.router, prefix=settings.api_v1_str)
api_router.include_router(
    car_operate.router,
    prefix=settings.api_v1_str,
    dependencies=Depends(get_current_user),
)
api_router.include_router(
    usage.router, prefix=settings.api_v1_str, dependencies=Depends(get_current_user)
)

app.include_router(api_router)

if __name__ == "__main__":
    # 2026 年推荐的启动方式：直接运行此脚本  # noqa: RUF003
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
