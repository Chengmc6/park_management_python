from fastapi import APIRouter

from app.api.v1.dependencies import UserDep
from app.api.v1.get_services import UserServiceDep
from app.common.api_response import ApiResponse
from app.schemas.user_dto.password_change_dto import UserPasswordChangeDto
from app.schemas.user_dto.user_login_request_dto import UserLoginRequestDto
from app.schemas.user_dto.user_register_dto import UserRegisterDto

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login")
async def login_for_access_token(
    login_data: UserLoginRequestDto, service: UserServiceDep
):
    response_data = service.authenticate_user(login_data)
    return ApiResponse.success(data=response_data)


@router.post("/register")
async def do_register(register_data: UserRegisterDto, service: UserServiceDep):
    service.register(register_data)
    return ApiResponse.success(message="注册成功")


@router.get("/me")
async def get_user_info(user: UserDep, service: UserServiceDep):
    user_info = service.get_user_info(user.id)  # type: ignore
    return ApiResponse.success(data=user_info)


@router.post("/change")
async def change_password(
    change_data: UserPasswordChangeDto, user: UserDep, service: UserServiceDep
):
    service.change_password(user_id=user.id, change_data=change_data)  # type: ignore
    return ApiResponse.success("修改成功,请重新登录")
