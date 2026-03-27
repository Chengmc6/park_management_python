from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- 基础配置 ---
    app_name: str = Field(default="park", description="应用名称")
    debug: bool = Field(default=False, alias="DEBUG", description="是否开启调试模式")

    # 数据库地址
    database_url: str = Field(
        default="mysql+pymysql://root:root@localhost:3306/park_management",
        alias="DATABASE_URL",
        description="数据库地址",
    )

    secret_key: str = Field(
        default="park-backend-jwt-secret-key-2025",
        description="加密密钥",
        alias="SECRET_KEY",
    )

    algorithm: str = Field(default="HS256", alias="ALGORITHM", description="加密算法")

    access_token_expire_time: int = Field(
        default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES", description="过期时间"
    )

    api_v1_str: str = Field(default="/api/v1")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略 .env 中多余的变量
    )


# 全局单例
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
