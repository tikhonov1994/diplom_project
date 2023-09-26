from typing import Callable, Awaitable

import pytest
import pytest_asyncio
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from settings import test_settings as config
from functional.test_data.mongo_data import test_movieLikes
from functional.utils.mongo import drop_collection, insert_data_to_collection


@pytest.fixture(scope='session')
def sync_mongo_client() -> MongoClient:
    _client = MongoClient(config.mongo_host,
                          config.mongo_port,
                          uuidRepresentation='standard')
    yield _client
    _client.close()


@pytest.fixture(scope='session', autouse=True)
def prepare_mongo(sync_mongo_client: MongoClient) -> None:
    # Здесь нужно будет дропнуть другие коллекции
    drop_collection(sync_mongo_client, config.social_mongo_database, 'movieLikes')
    ...
    # Здесь нужно будет добавить данные для тестов других коллекций
    insert_data_to_collection(sync_mongo_client, config.social_mongo_database, 'movieLikes', test_movieLikes)
    ...


@pytest.fixture(scope='session')
def mongo_client() -> AsyncIOMotorClient:
    _client = AsyncIOMotorClient(config.mongo_host,
                                 config.mongo_port,
                                 uuidRepresentation='standard')
    yield _client
    _client.close()


@pytest_asyncio.fixture(scope='session')
def add_data_to_collection(
        mongo_client: AsyncIOMotorClient
) -> Callable[[str, str, list[dict[str, any]]], Awaitable[None]]:
    async def inner(db_name: str, collection_name: str, data: list[dict[str, any]]) -> None:
        await mongo_client[db_name][collection_name].insert_many(data)

    return inner


@pytest_asyncio.fixture(scope='session')
def delete_data_from_collection(
        mongo_client: AsyncIOMotorClient
) -> Callable[[str, str, dict[str, any]], Awaitable[None]]:
    async def inner(db_name: str, collection_name: str, condition: dict[str, any]) -> None:
        await mongo_client[db_name][collection_name].delete_many(condition)

    return inner


@pytest_asyncio.fixture(scope='session')
def get_data_from_collection(
        mongo_client: AsyncIOMotorClient
) -> Callable[[str, str, dict[str, any]], Awaitable[list[dict[str, any]]]]:
    async def inner(db_name: str, collection_name: str, condition: dict[str, any]) -> list[dict[str, any]]:
        return await mongo_client[db_name][collection_name].find(condition).to_list(length=None)

    return inner
