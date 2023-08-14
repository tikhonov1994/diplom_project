from contextlib import asynccontextmanager

import uvicorn
from logging import config as logging_config
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from redis.backoff import ExponentialBackoff
from redis.asyncio.retry import Retry
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from sqlalchemy import create_engine
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from core.config import app_config as config
from core.logger import LOGGING
from api.v1 import users, roles, auth
from db import redis

logging_config.dictConfig(LOGGING)

origins = [
    "http://localhost",
    "http://localhost:8080",
]


# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     redis_retry = Retry(backoff=ExponentialBackoff(), retries=10)
#     redis.redis = Redis(host=config.redis_host, port=config.redis_port, retry=redis_retry,
#                               retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError])
#     yield
#     await redis.redis.close()

engine = create_engine(
    'postgresql+%s://%s:%s@%s:%s/%s' % (
        config.postgres_driver, config.postgres_user, config.postgres_password,
        config.postgres_host, config.postgres_port, config.postgres_db
    )
)

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

root_router = APIRouter(prefix='/auth/api')
root_router.include_router(users.router, prefix='/v1/users', tags=['users'])
root_router.include_router(roles.router, prefix='/v1/roles', tags=['roles'])
root_router.include_router(auth.router, prefix='/v1/auth', tags=['auth'])
app.include_router(root_router)


def add_token_header_to_auth_routes():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Auth service",
        version="2.5.0",
        description="Сервис авторизации",
        routes=app.routes,
    )

    # Custom documentation async-fastapi-jwt-auth
    headers = {
        "name": "jwt-token",
        "in": "header",
        "required": True,
        "schema": {"title": "auth-token", "type": "string"},
    }

    # Get routes from index 4 because before that fastapi define router for /openapi.json, /redoc, /docs, etc
    router_authorize = [
        route for route in app.routes[4:] if "auth_protected_routes" in route.tags
    ]

    for route in router_authorize:
        method = list(route.methods)[0].lower()
        try:
            openapi_schema["paths"][route.path][method]["parameters"].append(headers)
        except Exception:
            openapi_schema["paths"][route.path][method].update(
                {"parameters": [headers]}
            )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = add_token_header_to_auth_routes


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
