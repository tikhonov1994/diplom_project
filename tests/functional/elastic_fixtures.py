from typing import Awaitable, Callable
from uuid import UUID

import functional.test_data.es_data as data
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch, Elasticsearch
from functional.utils.elastic import (add_document_to_index, clear_indices,
                                      delete_document_from_index,
                                      insert_data_to_index, refresh_indices)
from settings import test_settings as settings


@pytest.fixture(scope='session')
def sync_elastic_client() -> Elasticsearch:
    _client = Elasticsearch(hosts=f'http://{settings.elastic_host}:{settings.elastic_port}')
    yield _client
    _client.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
def prepare_elastic(sync_elastic_client) -> None:
    clear_indices(sync_elastic_client)
    insert_data_to_index(sync_elastic_client, 'genres', data.test_genres)
    insert_data_to_index(sync_elastic_client, 'movies', data.test_films)
    insert_data_to_index(sync_elastic_client, 'persons', data.test_persons)
    refresh_indices(sync_elastic_client)


@pytest_asyncio.fixture(scope='session')
async def elastic_client() -> AsyncElasticsearch:
    # noinspection HttpUrlsUsage
    _es_client = AsyncElasticsearch(hosts=f'http://{settings.elastic_host}:{settings.elastic_port}')
    yield _es_client
    await _es_client.close()


@pytest_asyncio.fixture(scope='session')
def add_data_to_index(elastic_client) -> Callable[[str, UUID, dict[str, any]], Awaitable[None]]:
    async def inner(index: str, id_: UUID, document: dict[str, any]):
        await add_document_to_index(elastic_client, index, id_, document)

    return inner


@pytest_asyncio.fixture(scope='session')
def delete_data_from_index(elastic_client) -> Callable[[str, UUID], Awaitable[None]]:
    async def inner(index: str, id_: UUID):
        await delete_document_from_index(elastic_client, index, id_)

    return inner
