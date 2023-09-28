from datetime import datetime
from time import sleep
from uuid import uuid4, UUID

import pytest
from http import HTTPStatus

from functional.test_data.auth_data import test_auth_headers
from functional.test_data.db_data import test_user_info

pytestmark = pytest.mark.asyncio

ENDPOINT = '/social_api/api/v1/bookmarks/'


async def test_add_bookmark_auth(http_social_client) -> None:
    body = {'film_id': str(uuid4())}
    async with http_social_client.post(f'{ENDPOINT}add',
                                       json=body) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_add_bookmark(http_social_client, get_data_from_social_db) -> None:
    body = {'film_id': str(uuid4())}
    data_query = {'film_id': {'$eq': UUID(body['film_id'])}}

    assert not await get_data_from_social_db('bookmarks', data_query)

    async with http_social_client.post(f'{ENDPOINT}add',
                                       json=body,
                                       headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    data = await get_data_from_social_db('bookmarks', data_query)
    assert data
    assert data[0].get('film_id') == UUID(body.get('film_id'))


async def test_delete_bookmark_auth(http_social_client) -> None:
    async with http_social_client.delete(f'{ENDPOINT}{str(uuid4())}/delete') as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_delete_bookmark(http_social_client, add_data_to_social_db, get_data_from_social_db) -> None:
    bookmark_to_delete_id = uuid4()
    data = [{
        'user_id': UUID(test_user_info.get('id')),
        'bookmark_id': bookmark_to_delete_id,
        'film_id': uuid4(),
        'added': datetime.now()
    }]
    await add_data_to_social_db('bookmarks', data)
    assert await get_data_from_social_db('bookmarks', {'bookmark_id': {'$eq': bookmark_to_delete_id}})

    async with http_social_client.delete(f'{ENDPOINT}{str(bookmark_to_delete_id)}/delete',
                                         headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    assert not await get_data_from_social_db('bookmarks', {'bookmark_id': {'$eq': bookmark_to_delete_id}})


async def test_delete_not_existing_bookmark(http_social_client) -> None:
    async with http_social_client.delete(f'{ENDPOINT}{str(uuid4())}/delete',
                                         headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_get_user_bookmarks_auth(http_social_client) -> None:
    async with http_social_client.get(f'{ENDPOINT}') as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_get_user_bookmarks(http_social_client, get_data_from_social_db) -> None:
    user_id = UUID(test_user_info.get('id'))

    db_data = await get_data_from_social_db('bookmarks', {'user_id': {'$eq': user_id}})

    async with http_social_client.get(f'{ENDPOINT}',
                                      headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK
        response_data = await response.json()
        assert len(response_data) != 0
        assert len(response_data) == len(db_data)
