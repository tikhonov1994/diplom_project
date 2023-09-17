import asyncio

import pytest_asyncio
from aiohttp import ClientSession
from settings import test_settings as settings

from functional.test_data.auth_data import test_request_id_header

pytest_plugins = ('functional.elastic_fixtures', 'functional.redis_fixtures', 'functional.db_fixtures')


@pytest_asyncio.fixture(scope="session")
def event_loop():
    _loop = asyncio.get_event_loop()
    yield _loop
    if not _loop.is_closed():
        _loop.close()


@pytest_asyncio.fixture(scope='session')
async def http_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.api_host}:{settings.api_port}')
    yield _client
    await _client.close()


@pytest_asyncio.fixture(scope='session')
async def http_auth_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.auth_host}:{settings.auth_port}',
                            headers=test_request_id_header)
    _client.headers
    yield _client
    await _client.close()


@pytest_asyncio.fixture(scope='session')
async def http_ugc_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.ugc_host}:{settings.ugc_port}')
    yield _client
    await _client.close()
