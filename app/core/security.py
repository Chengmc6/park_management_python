from datetime import datetime, timedelta, timezone

import bcrypt
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
    extra_data: dict | None = None,
) -> str:
    """
    生成 JWT Token
    :param data: 需要加密到 payload 中的数据（通常包含 sub: username）
    :param expires_delta: 过期时间
    """  # noqa: RUF002

    # 设置token过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_time
        )

    # 注入标准声明 exp (Expiration Time)
    to_encode = {"sub": str(subject), "exp": expire, "iat": datetime.now(timezone.utc)}

    if extra_data:
        to_encode.update(extra_data)

    # 编码生成字符串
    encode_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encode_jwt


def decode_access_token(token: str):
    """
    解码 JWT Token，返回 payload
    返回 None 表示 token 无效或过期
    """  # noqa: RUF002
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except ExpiredSignatureError:
        raise
    except JWTError:
        raise
    except Exception:
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    校验明文密码与数据库哈希值是否匹配
    :param plain_password: 用户输入的明文
    :param hashed_password: 数据库存储的哈希串
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """使用 bcrypt 直接生成哈希"""
    # 自动处理 72 bytes 限制，并返回标准 bcrypt 字符串  # noqa: RUF003
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")
