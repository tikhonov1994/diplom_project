import uuid

from http import HTTPStatus
import pytest
from aiohttp.client import ClientSession

from functional.test_data.es_data import test_films, FANTASY_GENRE_FILM, FILM_FOR_TEST_CACHE
from functional.test_data.auth_data import test_auth_headers

ENDPOINT = '/content/api/v1/films/'

pytestmark = pytest.mark.asyncio


async def test_get_by_id_auth(http_client: ClientSession) -> None:
    film_id = test_films[0]["id"]
    async with http_client.get(ENDPOINT + str(film_id)) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_get_by_id(http_client: ClientSession) -> None:
    film_id = test_films[0]["id"]
    async with http_client.get(ENDPOINT + str(film_id), headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK
        data = await response.json()
        assert data['id'] == film_id


async def test_return_not_found_on_invalid_id(http_client) -> None:
    async with http_client.get(ENDPOINT + str(uuid.uuid4().hex), headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_get_list_with_sorting(http_client) -> None:
    params = {'sort': 'imdb_rating'}
    async with http_client.get(url=ENDPOINT, params=params) as response:
        data = await response.json()

        assert response.status == HTTPStatus.OK
        assert len(data['results']) != 0
        for i in range(len(data['results']) - 1):
            assert data['results'][i]['imdb_rating'] <= data['results'][i + 1]['imdb_rating']


async def test_get_list_with_overflow_page_value(http_client) -> None:
    params = {
        "page_number": 100,
        "page_size": 50,
    }
    async with http_client.get(url=ENDPOINT, params=params) as response:
        data = await response.json()

        assert response.status == HTTPStatus.OK
        assert len(data['results']) == 0


async def test_get_list_with_pagination(http_client) -> None:
    params = {
        "page_number": 2,
        "page_size": 1,
    }
    async with http_client.get(url=ENDPOINT, params=params) as response:
        data = await response.json()

        assert response.status == HTTPStatus.OK
        assert len(data['results']) == 1
        assert data['prev'] == 1
        assert data['results'][0]['id'] == test_films[1]['id']


async def test_get_list_with_invalid_sorting_value(http_client) -> None:
    params = {'sort': 'invalid_sort'}
    async with http_client.get(url=ENDPOINT, params=params) as response:
        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_films_with_genre_filter(http_client) -> None:
    genre_id = FANTASY_GENRE_FILM['genre'][0]['id']
    params = {
        "page_number": 1,
        "page_size": 1,
        'genre': genre_id,
    }
    async with http_client.get(url=ENDPOINT, params=params) as response:
        data = await response.json()

        assert response.status == HTTPStatus.OK
        assert data['results'][0]['genre'][0]['id'] == genre_id


async def test_get_by_id_from_cache(http_client, add_data_to_index, delete_data_from_index) -> None:
    endpoint = ENDPOINT + str(FILM_FOR_TEST_CACHE['id'])
    async with http_client.get(endpoint, headers=test_auth_headers) as new_response:
        assert new_response.status == 404

    await add_data_to_index(index='movies', id_=FILM_FOR_TEST_CACHE['id'], document=FILM_FOR_TEST_CACHE)

    async with http_client.get(endpoint, headers=test_auth_headers) as new_response:
        assert new_response.status == 200

    await delete_data_from_index(index='movies', id_=FILM_FOR_TEST_CACHE['id'])

    async with http_client.get(endpoint, headers=test_auth_headers) as new_response:
        new_data = await new_response.json()
        assert new_response.status == 200
        assert new_data.get('id') == FILM_FOR_TEST_CACHE['id']
