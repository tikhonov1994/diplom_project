from contextlib import asynccontextmanager

import uvicorn
from logging import config as logging_config
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from redis.backoff import ExponentialBackoff
from redis.asyncio.retry import Retry
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError

from api.v1 import films, genres, persons
from core.config import app_config as config
from db.storage.backends import elastic
from db import redis_cache
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_retry = Retry(backoff=ExponentialBackoff(), retries=10)
    redis_cache.redis = Redis(host=config.redis_host, port=config.redis_port, retry=redis_retry,
                              retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError])
    elastic.es = AsyncElasticsearch(hosts=[f'http://{config.elastic_host}:{config.elastic_port}'],
                                    retry_on_timeout=True)
    FastAPICache.init(RedisBackend(redis_cache.redis), prefix="fastapi-cache")
    yield
    await redis_cache.redis.close()
    await elastic.es.close()


app = FastAPI(
    title=config.api.project_name,
    docs_url='/content/api/openapi',
    openapi_url='/content/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
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
