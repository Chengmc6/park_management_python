from pydantic import BaseModel, Field, field_validator


class UserLoginRequestDto(BaseModel):
    # min_length=1 自动处理非空字符串检查
    username: str = Field(..., min_length=1, description="请输入用户名")
    password: str = Field(..., min_length=1, description="请输入密码")

    @field_validator("username", "password")  # 可以同时对多个字段生效
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            cleaned = v.strip()
            if not cleaned:
                raise ValueError("不能为空字符串")
            return cleaned
        return v
