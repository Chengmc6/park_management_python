from pydantic import BaseModel, Field, field_validator


class UserRegisterDto(BaseModel):
    username: str = Field(..., min_length=1, description="请输入用户名")
    password: str = Field(
        ..., min_length=6, max_length=18, description="请输入6-18位的密码"
    )

    @field_validator("username", "password")
    @classmethod
    def validate_field(cls, v: str) -> str:
        if isinstance(v, str):
            cleaned = v.strip()
            if not cleaned:
                raise ValueError("不能为空字符")
            return cleaned
        return v
