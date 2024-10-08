import uvicorn

from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from redis.backoff import ExponentialBackoff
from redis.asyncio.retry import Retry
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from starlette import status
import sentry_sdk

from api.v1 import films, genres, persons
from core.config import app_config as config
from core.auth import AuthExceptionBase
from db.storage.backends import elastic
from db import redis_cache
from core.middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_retry = Retry(backoff=ExponentialBackoff(), retries=10)
    redis_cache.redis = Redis(host=config.redis_host, port=config.redis_port, retry=redis_retry,
                              retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError])
    # noinspection HttpUrlsUsage
    elastic.es = AsyncElasticsearch(hosts=[f'http://{config.elastic_host}:{config.elastic_port}'],
                                    retry_on_timeout=True)
    FastAPICache.init(RedisBackend(redis_cache.redis),
                      prefix="fastapi-cache",
                      key_builder=redis_cache.request_key_builder)
    yield
    await redis_cache.redis.close()
    await elastic.es.close()


if config.export_logs:
    sentry_sdk.init(
        dsn=config.sentry.dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )

app = FastAPI(
    title=config.api.project_name,
    docs_url='/content/api/openapi',
    openapi_url='/content/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.middleware('http')(LoggingMiddleware())


@app.exception_handler(AuthExceptionBase)
async def auth_exception_handler(_: Request, exc: AuthExceptionBase):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'message': str(exc)},
    )


root_router = APIRouter(prefix='/content/api')
root_router.include_router(films.router, prefix='/v1/films', tags=['films'])
root_router.include_router(genres.router, prefix='/v1/genres', tags=['genres'])
root_router.include_router(persons.router, prefix='/v1/persons', tags=['persons'])
app.include_router(root_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
