from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader
from jose import ExpiredSignatureError, JWTError
from sqlmodel import Session, select

from app.common.result_code import ResultCode

# from app.core.config import settings
from app.core.security import decode_access_token
from app.db.database import get_session
from app.exception.business_exception import BusinessException
from app.models.user import User

# 定义提取器：告诉 FastAPI 去 /login 接口拿 Token  # noqa: RUF003
# oauth2_scheme = OAuth2PasswordBearer(
#    tokenUrl=f"{settings.api_v1_str}/auth/login",
#    scheme_name="OAuth2",  # 在 Swagger 中显示更清晰
#    description="在 Authorization 头中传入 Bearer Token",
# )
oauth2_scheme = APIKeyHeader(name="Authorization", description="格式：Bearer <Token>")  # noqa: RUF001


async def get_current_user(
    db: Session = Depends(get_session),  # noqa: B008
    token: str = Depends(oauth2_scheme),
) -> User:
    print("=== get_current_user 被调用 ===")
    print(f"收到的原始 token: {token[:50]}...")
    try:
        # 去掉 Bearer 前缀
        if token.startswith("Bearer "):
            token = token[7:].strip()
        # 解码jwt
        payload = decode_access_token(token)
        if payload is None:
            raise BusinessException(ResultCode.UNAUTHORIZED)
        user_data = payload.get("sub")
        if not user_data:
            raise BusinessException(
                ResultCode.UNAUTHORIZED,
                message="格式出错，缺少用户信息",  # noqa: RUF001
            )
    except ExpiredSignatureError:
        raise BusinessException(ResultCode.UNAUTHORIZED, "token已过期")  # noqa: B904
    except JWTError:
        raise BusinessException(ResultCode.UNAUTHORIZED, "解析出错")  # noqa: B904
    except Exception:
        raise BusinessException(ResultCode.UNKNOWN_ERROR)  # noqa: B904

    # 数据库验证
    user = db.exec(select(User).where(User.username == user_data)).first()

    if not user:
        raise BusinessException(ResultCode.USER_NOT_FOUND)

    if user.is_deleted == 1:
        raise BusinessException(ResultCode.FORBIDDEN)

    return user


# 1. 定义一个类型别名（“模块级”配置思想）  # noqa: RUF003
# 这种写法完全避开了在函数签名里写 Depends() 调用
DbDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[User, Depends(get_current_user)]


async def get_current_admin(current_user: UserDep) -> User:
    if current_user.role != 1:
        raise BusinessException(ResultCode.ILLEGAL_PERMISSION)
    return current_user


AdminDep = Annotated[User, Depends(get_current_admin)]
