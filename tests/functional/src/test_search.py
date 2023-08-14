import pytest
from http import HTTPStatus

from functional.test_data.auth_data import test_auth_headers

pytestmark = pytest.mark.asyncio


async def test_search_films_auth(http_client) -> None:
    params = {
        'query': 'Star Wars',
        'page_number': 1,
        'page_size': 25
    }
    async with http_client.get(url=f'/content/api/v1/films/search/', params=params) as response:
        assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    'search_query, expected_answer',
    [
        (
                {'query': 'Star Wars'},
                {'status_code': HTTPStatus.OK, 'body_length': 3},
        ),
        (
                {'query': 'The Clone'},
                {'status_code': HTTPStatus.OK, 'body_length': 1},
        ),
    ]
)
async def test_search_films_by_title(http_client, search_query, expected_answer) -> None:
    params = {
        'query': search_query['query'],
        'page_number': 1,
        'page_size': 25
    }
    async with http_client.get(url=f'/content/api/v1/films/search/', params=params,
                               headers=test_auth_headers) as response:
        data = await response.json()

        assert response.status == expected_answer['status_code']
        assert len(data['results']) == expected_answer['body_length']


@pytest.mark.parametrize(
    'search_query, expected_answer',
    [
        (
                {'query': 'george'},
                {'status_code': HTTPStatus.OK, 'body_length': 1},
        ),
    ]
)
async def test_search_films_by_person(http_client, search_query, expected_answer) -> None:
    params = {
        'query': search_query['query'],
        'page_number': 1,
        'page_size': 25
    }
    async with http_client.get(url=f'/content/api/v1/persons/search/', params=params) as response:
        data = await response.json()

        assert response.status == expected_answer['status_code']
        assert len(data['results']) == expected_answer['body_length']
