from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import app_config
from db.storage.generic_storage import GenericStorage
from db.model import UserInfo

__engine = create_async_engine(app_config.postgres_dsn_async)
__session = async_sessionmaker(__engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    session = __session()
    try:
        yield session
    finally:
        await session.close()


DbSessionDep = Annotated[AsyncSession, Depends(get_session)]
UserInfoStorageDep = Annotated[GenericStorage[UserInfo], Depends()]
