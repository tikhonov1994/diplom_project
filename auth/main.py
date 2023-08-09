from contextlib import asynccontextmanager

import uvicorn
from logging import config as logging_config
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from sqlalchemy import create_engine

from core.config import app_config as config
from core.logger import LOGGING
from api.v1 import users, roles, auth
from db import redis_db
from redis.asyncio import Redis

logging_config.dictConfig(LOGGING)

engine = create_engine(
    'postgresql+%s://%s:%s@%s:%s/%s' % (
        config.postgres_driver, config.postgres_user, config.postgres_password,
        config.postgres_host, config.postgres_port, config.postgres_db
    )
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_db.redis = Redis(host=config.redis_host, port=config.redis_port, db=0, decode_responses=True)
    yield
    await redis_db.redis.close()

# app = FastAPI(
#     title=config.api.project_name,
#     docs_url='/auth/api/openapi',
#     openapi_url='/auth/api/openapi.json',
#     default_response_class=ORJSONResponse,
#     lifespan=lifespan,
# )

app = FastAPI(
    title=config.api.project_name,
    docs_url='/auth/api/openapi',
    openapi_url='/auth/api/openapi.json',
    default_response_class=ORJSONResponse,
    # lifespan=lifespan,
)

root_router = APIRouter(prefix='/auth/api')
root_router.include_router(users.router, prefix='/v1/users', tags=['users'])
root_router.include_router(roles.router, prefix='/v1/roles', tags=['roles'])
root_router.include_router(auth.router, prefix='/v1/auth', tags=['auth'])
app.include_router(root_router)

if __name__ == '__main__':
    # uvicorn.run(
    #     'main:app',
    #     host=config.api.host,
    #     port=config.api.port,
    # )

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
