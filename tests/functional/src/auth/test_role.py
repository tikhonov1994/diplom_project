import time
import uuid
from http import HTTPStatus

import pytest
from aiohttp import ClientSession
from functional.test_data.auth_data import test_auth_headers, test_admin_auth_headers
from functional.test_data.db_data import test_user_info
from functional.utils.db import get_from_db, insert_into_db
from sqlalchemy.ext.asyncio import AsyncSession

ENDPOINT = '/auth/api/v1/roles/'
pytestmark = pytest.mark.asyncio


async def test_add_role_auth(http_auth_client: ClientSession) -> None:
    new_role_name = 'unauthorized_role'

    async with http_auth_client.post(ENDPOINT, json={'name': new_role_name}) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED

    async with http_auth_client.post(ENDPOINT, json={'name': new_role_name}, headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_add_role(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    new_role_name = 'new_role'

    assert await get_from_db(db_session, 'user_role', ('name', new_role_name), 'auth') is None

    async with http_auth_client.post(ENDPOINT,
                                     json={'name': new_role_name},
                                     headers=test_admin_auth_headers) as response:
        assert response.status == HTTPStatus.OK
        _ = await response.json()

    # wait for auth service to commit changes
    time.sleep(0.2)

    role_in_db = await get_from_db(db_session, 'user_role', ('name', new_role_name), 'auth')
    assert role_in_db is not None
    assert role_in_db['name'] == new_role_name


async def test_add_role_conflict(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    new_role_name = 'new_conflicting_role'

    assert await get_from_db(db_session, 'user_role', ('name', new_role_name), 'auth') is None

    async with http_auth_client.post(ENDPOINT,
                                     json={'name': new_role_name},
                                     headers=test_admin_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    async with http_auth_client.post(ENDPOINT,
                                     json={'name': new_role_name},
                                     headers=test_admin_auth_headers) as response:
        assert response.status == HTTPStatus.CONFLICT


async def test_get_roles_auth(http_auth_client: ClientSession) -> None:
    async with http_auth_client.get(ENDPOINT) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED

    async with http_auth_client.get(ENDPOINT, headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_get_roles(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    id_1, id_2 = str(uuid.uuid4()), str(uuid.uuid4())
    name_1, name_2 = 'user_role_1', 'user_role_2'
    await insert_into_db(db_session, 'user_role', {'id': id_1, 'name': name_1}, 'auth')
    await insert_into_db(db_session, 'user_role', {'id': id_2, 'name': name_2}, 'auth')

    async with http_auth_client.get(ENDPOINT, headers=test_admin_auth_headers) as response:
        assert response.status == HTTPStatus.OK
        data = await response.json()
        assert len(data) >= 2
        ids = [item['id'] for item in data]
        names = [item['name'] for item in data]
        assert id_1 in ids
        assert id_2 in ids
        assert name_1 in names
        assert name_2 in names


async def test_delete_role_auth(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    id_to_delete = str(uuid.uuid4())
    await insert_into_db(db_session,
                         'user_role',
                         {'id': id_to_delete, 'name': 'role_cant_delete_without_auth'},
                         'auth')

    async with http_auth_client.delete(ENDPOINT + id_to_delete) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED

    async with http_auth_client.delete(ENDPOINT + id_to_delete, headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_delete_role(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    id_to_delete = str(uuid.uuid4())
    await insert_into_db(db_session, 'user_role', {'id': id_to_delete, 'name': 'role_to_delete'}, 'auth')

    async with http_auth_client.delete(ENDPOINT + id_to_delete,
                                       headers=test_admin_auth_headers) as response:
        assert response.status == HTTPStatus.OK
        _ = await response.json()

    # wait for auth service to commit changes
    time.sleep(0.2)

    assert await get_from_db(db_session, 'user_role', ('id', id_to_delete), 'auth') is None


async def test_delete_not_existing_role(http_auth_client: ClientSession) -> None:
    async with http_auth_client.delete(ENDPOINT + str(uuid.uuid4()),
                                       headers=test_admin_auth_headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_delete_role_conflict(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    assert await get_from_db(db_session, 'user_info', ('id', test_user_info['id']), 'auth') is not None
    assert await get_from_db(db_session, 'user_role', ('id', test_user_info['user_role_id']), 'auth') is not None

    async with http_auth_client.delete(ENDPOINT + test_user_info['user_role_id'],
                                       headers=test_admin_auth_headers) as response:
        assert response.status == HTTPStatus.CONFLICT
