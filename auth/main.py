from contextlib import asynccontextmanager

import uvicorn
from logging import config as logging_config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from redis.backoff import ExponentialBackoff
from redis.asyncio.retry import Retry
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from sqlalchemy import create_engine

from core.config import app_config as config
from core.logger import LOGGING
from api.v1 import users, roles
from db.redis import redis

logging_config.dictConfig(LOGGING)


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_retry = Retry(backoff=ExponentialBackoff(), retries=10)
    redis = Redis(host=config.redis_host, port=config.redis_port, retry=redis_retry,
                              retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError])
    yield
    await redis.close()

engine = create_engine(
    'postgresql+%s://%s:%s@%s:%s/%s' % (
        config.postgres_driver, config.postgres_user, config.postgres_password,
        config.postgres_host, config.postgres_port, config.postgres_db
    )
)

app = FastAPI(
    title=config.api.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
app.include_router(roles.router, prefix='/api/v1/roles', tags=['roles'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
