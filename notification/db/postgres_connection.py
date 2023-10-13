from typing import Annotated

from core.config import app_config
from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

__engine = create_async_engine(app_config.postgres_dsn)
__session = async_sessionmaker(__engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    session = __session()
    # noinspection PyBroadException
    try:
        yield session
        await session.commit()
    finally:
        await session.close()


DbSessionDep = Annotated[AsyncSession, Depends(get_session)]
