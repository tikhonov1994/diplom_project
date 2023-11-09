import asyncio
from typing import AsyncGenerator

import pytest_asyncio
from aiohttp import ClientSession
from functional.test_data.auth_data import test_request_id_header
from settings import test_settings as settings

pytest_plugins = ('functional.elastic_fixtures',
                  'functional.redis_fixtures',
                  'functional.db_fixtures',
                  'functional.mongo_fixtures',
                  'functional.minio_fixtures')


@pytest_asyncio.fixture(scope="session")
def event_loop():
    _loop = asyncio.get_event_loop()
    yield _loop
    if not _loop.is_closed():
        _loop.close()


@pytest_asyncio.fixture(scope='session')
async def http_client() -> AsyncGenerator[ClientSession, None]:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.api_host}:{settings.api_port}')
    yield _client
    await _client.close()


@pytest_asyncio.fixture(scope='session')
async def http_auth_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.auth_host}:{settings.auth_port}',
                            headers=test_request_id_header)
    yield _client
    await _client.close()


@pytest_asyncio.fixture(scope='session')
async def http_ugc_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.ugc_host}:{settings.ugc_port}')
    yield _client
    await _client.close()


@pytest_asyncio.fixture(scope='session')
async def http_social_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.social_host}:{settings.social_port}')
    yield _client
    await _client.close()


@pytest_asyncio.fixture(scope='session')
async def http_notification_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.notification_host}:{settings.notification_port}')
    yield _client
    await _client.close()


@pytest_asyncio.fixture(scope='session')
async def http_user_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.user_host}:{settings.user_port}')
    yield _client
    await _client.close()


@pytest_asyncio.fixture(scope='session')
async def http_minio_client() -> ClientSession:
    # noinspection HttpUrlsUsage
    _client = ClientSession(base_url=f'http://{settings.minio_host}:{settings.minio_port}')
    yield _client
    await _client.close()
