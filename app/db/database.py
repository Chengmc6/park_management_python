from contextlib import contextmanager

from sqlmodel import Session, create_engine

from app.core.config import settings

# 创建连接引擎
engine = create_engine(
    settings.database_url,  # 连接地址
    echo=settings.debug,  # 只有在 debug=True 时才打印 SQL
    pool_pre_ping=True,  # 防止连接池中的连接失效（推荐）  # noqa: RUF003
    pool_size=20,  # 连接池大小（可根据实际情况调整）  # noqa: RUF003
    max_overflow=10,  # 超出 pool_size 后最多再创建的连接数
)


@contextmanager
def get_db():
    """推荐的上下文管理器方式"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# 创建获取 Session 的函数
# 在此自动执行提交，失败进行回滚  # noqa: RUF003
def get_session():
    with get_db() as session:
        yield session


def get_db_session():  # FastAPI 专用版本,Depends可以处理yield的生命周期
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


# 如果未来要使用异步（推荐提前准备）  # noqa: RUF003
# async def get_session_async():
#     async with Session(engine) as session:
#         yield session
