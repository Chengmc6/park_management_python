import uvicorn
from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.dependencies import get_current_user
from app.api.v1.endpoints import auth, car_operate, usage
from app.core.config import settings
from app.exception.exception_handler import exception_handler

app = FastAPI(title=settings.app_name, debug=settings.debug)

# 1. 定义允许的源（Origin）  # noqa: RUF003
# 在开发阶段，可以用 ["*"] 允许所有，但生产环境建议写死前端域名  # noqa: RUF003
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# 2. 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许跨域的源列表
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],  # 允许的 HTTP 方法 (GET, POST, PUT, DELETE 等)
    allow_headers=["*"],  # 允许的 Header (如 Authorization, Content-Type)
)

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
