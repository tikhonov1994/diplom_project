import pytest_asyncio
from functional.utils.redis import clear_cache
from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from settings import test_settings as settings


@pytest_asyncio.fixture(scope='session')
def sync_redis_client() -> Redis:
    _client = Redis(host=settings.redis_host, port=settings.redis_port)
    yield _client
    _client.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
def prepare_redis(sync_redis_client) -> None:
    clear_cache(sync_redis_client)


@pytest_asyncio.fixture(scope='session')
async def redis_client() -> AsyncRedis:
    _r_client = AsyncRedis(host=settings.redis_host, port=settings.redis_port)
    yield _r_client
    await _r_client.close()
