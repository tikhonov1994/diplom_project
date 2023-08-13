from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from http import HTTPStatus
import uuid

from functional.utils.db import insert_into_db, get_from_db, clear_db_table
from functional.test_data.db_data import test_user_info

ENDPOINT = '/auth/api/v1/roles/'
pytestmark = pytest.mark.asyncio


async def test_add_role(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    new_role_name = 'new_role'

    assert await get_from_db(db_session, 'user_role', ('name', new_role_name), 'auth') is None

    async with http_auth_client.post(ENDPOINT, json={'name': new_role_name}) as response:
        assert response.status == HTTPStatus.OK
        # wait for response from client, so get_from_db() will run strictly after Auth services' session commit
        _ = await response.json()

    role_in_db = await get_from_db(db_session, 'user_role', ('name', new_role_name), 'auth')
    assert role_in_db is not None
    assert role_in_db['name'] == new_role_name


async def test_add_role_conflict(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    new_role_name = 'new_conflicting_role'

    assert await get_from_db(db_session, 'user_role', ('name', new_role_name), 'auth') is None

    async with http_auth_client.post(ENDPOINT, json={'name': new_role_name}) as response:
        assert response.status == HTTPStatus.OK

    async with http_auth_client.post(ENDPOINT, json={'name': new_role_name}) as response:
        assert response.status == HTTPStatus.CONFLICT


async def test_get_roles(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    id_1, id_2 = str(uuid.uuid4()), str(uuid.uuid4())
    name_1, name_2 = 'user_role_1', 'user_role_2'
    await clear_db_table(db_session, 'user_role', 'auth')
    await insert_into_db(db_session, 'user_role', {'id': id_1, 'name': name_1}, 'auth')
    await insert_into_db(db_session, 'user_role', {'id': id_2, 'name': name_2}, 'auth')

    async with http_auth_client.get(ENDPOINT) as response:
        assert response.status == HTTPStatus.OK
        data = await response.json()
        assert len(data) == 2
        data.sort(key=lambda x: x['name'])
        item1, item2 = data
        assert str(item1['id']) == id_1
        assert str(item2['id']) == id_2
        assert item1['name'] == name_1
        assert item2['name'] == name_2


async def test_delete_role(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    id_to_delete = str(uuid.uuid4())
    await insert_into_db(db_session, 'user_role', {'id': id_to_delete, 'name': 'role_to_delete'}, 'auth')

    async with http_auth_client.delete(ENDPOINT + id_to_delete) as response:
        assert response.status == HTTPStatus.OK

    assert await get_from_db(db_session, 'user_role', ('id', id_to_delete), 'auth') is None


async def test_delete_not_existing_role(http_auth_client: ClientSession) -> None:
    async with http_auth_client.delete(ENDPOINT + str(uuid.uuid4())) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_delete_role_conflict(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    id_to_delete = str(uuid.uuid4())
    test_user = test_user_info.copy()
    test_user['user_role_id'] = id_to_delete

    await insert_into_db(db_session, 'user_role', {'id': id_to_delete, 'name': 'role_with_conflict'}, 'auth')
    await insert_into_db(db_session, 'user_info', test_user, 'auth')

    async with http_auth_client.delete(ENDPOINT + id_to_delete) as response:
        assert response.status == HTTPStatus.CONFLICT
