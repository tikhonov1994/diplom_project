from contextlib import asynccontextmanager

import uvicorn
import sentry_sdk

from utils.rate_limiter import throttle
from core.config import app_config as config
from core.middleware import LoggingMiddleware
from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from utils.tracer import configure_tracer
from api.v1 import auth, roles, users
from db import redis

if config.export_logs:
    sentry_sdk.init(
        dsn=config.sentry.dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_retry = Retry(backoff=ExponentialBackoff(), retries=10)
    redis.redis = Redis(host=config.redis_host, port=config.redis_port, retry=redis_retry,
                        retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError])
    yield
    await redis.redis.close()


app = FastAPI(
    title=config.api.project_name,
    docs_url='/auth/api/openapi',
    openapi_url='/auth/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.middleware('http')(LoggingMiddleware())
configure_tracer(app)
throttle(app)

root_router = APIRouter(prefix='/auth/api')
root_router.include_router(users.router, prefix='/v1/users', tags=['users'])
root_router.include_router(roles.router, prefix='/v1/roles', tags=['roles'])
root_router.include_router(auth.router, prefix='/v1/auth', tags=['auth'])
app.include_router(root_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
