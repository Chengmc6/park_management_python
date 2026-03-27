from datetime import datetime

from sqlmodel import Field, SQLModel, text


class User(SQLModel, table=True):
    __tablename__: str = "user"
    id: int | None = Field(default=None, primary_key=True)  # user_id
    username: str  # 登录用户名,not null
    password: str  # 密码,not null
    role: int = Field(default=0)  # 角色:普通和管理员(user,admin)
    is_deleted: int = Field(default=0)  # 逻辑删除标识(0未删除,1已删除)
    created_at: datetime | None = Field(
        default=None, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )  # 创建时间
    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },
    )  # 更新时间
