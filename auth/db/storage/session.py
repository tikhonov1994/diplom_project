from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import app_config

__engine = create_async_engine(app_config.postgres_dsn)
__session = async_sessionmaker(__engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    session = __session()
    try:
        yield session
    except:
        await session.close()
    finally:
        await session.commit()
        await session.close()


DbSessionDep = Annotated[AsyncSession, Depends(get_session)]
