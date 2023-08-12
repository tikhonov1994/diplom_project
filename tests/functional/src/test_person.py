import pytest
import uuid

from http import HTTPStatus

from functional.test_data.es_data import test_persons

ENDPOINT = '/content/api/v1/persons/'
pytestmark = pytest.mark.asyncio


async def test_get_by_id(http_client) -> None:
    async with http_client.get(f'{ENDPOINT}{test_persons[0]["id"]}') as response:
        data = await response.json()
        assert response.status == HTTPStatus.OK
        assert data.get('full_name') == 'George Lucas'


async def test_get_invalid_id(http_client) -> None:
    async with http_client.get(f'{ENDPOINT}{uuid.uuid4().hex}') as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_get_films_by_person_id(http_client) -> None:
    async with http_client.get(f'{ENDPOINT}{test_persons[0]["id"]}/film') as response:
        data = await response.json()
        assert response.status == HTTPStatus.OK
        assert len(data) == 2
        assert data[0].get('title') == 'Star Wars: Episode VI - Return of the Jedi'


async def test_get_by_id_from_cache(http_client, add_data_to_index, delete_data_from_index) -> None:
    test_person = {'id': '32c426ed-69d8-4306-829a-1aa8f3363b2c', 'full_name': 'Test Person', 'films': []}

    async with http_client.get(f'{ENDPOINT}{test_person.get("id")}') as new_response:
        assert new_response.status == HTTPStatus.NOT_FOUND

    await add_data_to_index(index='persons', id_=test_person['id'], document=test_person)

    # Почему то в кэш запись попадает только после второго успешного запроса
    async with http_client.get(f'{ENDPOINT}{test_person.get("id")}') as new_response:
        assert new_response.status == HTTPStatus.OK
    async with http_client.get(f'{ENDPOINT}{test_person.get("id")}') as new_response:
        assert new_response.status == HTTPStatus.OK

    await delete_data_from_index(index='persons', id_=test_person['id'])

    async with http_client.get(f'{ENDPOINT}{test_person.get("id")}') as new_response:
        new_data = await new_response.json()
        assert new_response.status == HTTPStatus.OK
        assert new_data.get('full_name') == 'Test Person'
