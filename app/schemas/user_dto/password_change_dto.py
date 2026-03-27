from pydantic import BaseModel, Field, field_validator


class UserPasswordChangeDto(BaseModel):
    old_password: str = Field(..., min_length=1, description="请输入旧密码")
    new_password: str = Field(
        ..., min_length=6, max_length=18, description="请输入6-18位的新密码"
    )

    @field_validator("old_password", "new_password")
    @classmethod
    def validate_field(cls, v: str) -> str:
        if isinstance(v, str):
            cleaned = v.strip()
            if not cleaned:
                raise ValueError("不能输入空字符")
            return cleaned
        return v
