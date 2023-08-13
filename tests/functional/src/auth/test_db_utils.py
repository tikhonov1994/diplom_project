import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from functional.utils.db import insert_into_db, delete_from_db, get_from_db, clear_db_table

pytestmark = pytest.mark.asyncio


async def test_db_utils_examples(db_session: AsyncSession) -> None:
    _id = str(uuid.uuid4())

    # insert into table
    await insert_into_db(db_session, 'user_role', {'id': _id, 'name': 'new'}, 'auth')

    # get by id
    item = await get_from_db(db_session, 'user_role', ('id', _id), 'auth')
    assert str(item['id']) == _id
    assert item['name'] == 'new'

    # delete by id
    await delete_from_db(db_session, 'user_role', ('id', _id), 'auth')

    # get when item doesn't exist (return none)
    item = await get_from_db(db_session, 'user_role', ('id', _id), 'auth')
    assert item is None

    # delete when item doesn't exist (nothing happens)
    await delete_from_db(db_session, 'user_role', ('id', uuid.uuid4()), 'auth')

    # insert again
    await insert_into_db(db_session, 'user_role', {'id': str(uuid.uuid4()), 'name': 'newest'}, 'auth')

    # get by arbitrary field
    item = await get_from_db(db_session, 'user_role', ('name', 'newest'), 'auth')
    assert item['name'] == 'newest'

    # delete by arbitrary field
    await delete_from_db(db_session, 'user_role', ('name', 'newest'), 'auth')

    # delete all table records
    await insert_into_db(db_session, 'user_role', {'id': str(uuid.uuid4()), 'name': 'user_role_1'}, 'auth')
    await insert_into_db(db_session, 'user_role', {'id': str(uuid.uuid4()), 'name': 'user_role_2'}, 'auth')
    assert await get_from_db(db_session, 'user_role', ('name', 'user_role_1'), 'auth') is not None
    assert await get_from_db(db_session, 'user_role', ('name', 'user_role_2'), 'auth') is not None
    await clear_db_table(db_session, 'user_role', 'auth')
    assert await get_from_db(db_session, 'user_role', ('name', 'user_role_1'), 'auth') is None
    assert await get_from_db(db_session, 'user_role', ('name', 'user_role_2'), 'auth') is None
