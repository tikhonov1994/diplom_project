import uuid
from http import HTTPStatus

import pytest
from functional.test_data.auth_data import test_auth_headers
from functional.test_data.es_data import test_genres

ENDPOINT = '/content/api/v1/genres/'
pytestmark = pytest.mark.asyncio


async def test_get_by_id_auth(http_client) -> None:
    async with http_client.get(f'{ENDPOINT}{test_genres[0]["id"]}') as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_get_by_id(http_client) -> None:
    async with http_client.get(f'{ENDPOINT}{test_genres[0]["id"]}', headers=test_auth_headers) as response:
        data = await response.json()
        assert response.status == HTTPStatus.OK
        assert data.get('name') == 'Action'


async def test_return_not_found_on_invalid_id(http_client) -> None:
    async with http_client.get(f'{ENDPOINT}{uuid.uuid4().hex}', headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_get_list(http_client) -> None:
    async with http_client.get(ENDPOINT) as response:
        data = await response.json()
        assert len(data) == 2


async def test_get_by_id_from_cache(http_client, add_data_to_index, delete_data_from_index) -> None:
    test_genre = {'id': '74631ed6-a592-4980-b510-7b1f74373969', 'name': 'test_genre'}

    async with http_client.get(f'{ENDPOINT}{test_genre.get("id")}', headers=test_auth_headers) as new_response:
        assert new_response.status == HTTPStatus.NOT_FOUND

    await add_data_to_index(index='genres', id_=test_genre['id'], document=test_genre)

    async with http_client.get(f'{ENDPOINT}{test_genre.get("id")}', headers=test_auth_headers) as new_response:
        assert new_response.status == HTTPStatus.OK

    await delete_data_from_index(index='genres', id_=test_genre['id'])

    async with http_client.get(f'{ENDPOINT}{test_genre.get("id")}', headers=test_auth_headers) as new_response:
        new_data = await new_response.json()
        assert new_response.status == HTTPStatus.OK
        assert new_data.get('name') == 'test_genre'
