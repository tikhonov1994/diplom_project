import pytest
import pytest_asyncio
from functional.test_data.db_data import (test_admin_info, test_admin_role,
                                          test_user_info, test_user_role)
from functional.utils.db import insert_into_db
from settings import test_settings as config
from sqlalchemy import Engine, MetaData, create_engine, inspect, text
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)


@pytest_asyncio.fixture(scope='session')
async def db_engine() -> AsyncEngine:
    engine = create_async_engine(config.postgres_dsn, future=True)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope='session')
def db_engine_sync() -> Engine:
    engine = create_engine(config.postgres_dsn, future=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope='session', autouse=True)
def db_clean_up(db_engine_sync) -> None:
    db_engine_sync: Engine
    _conn = db_engine_sync.connect()

    inspector = inspect(db_engine_sync)
    schemas = inspector.get_schema_names()

    allowed_schemas = ['public',
                       'content',
                       config.auth_db_schema]

    prohibited_tables = ['alembic_version']

    for schema in schemas:
        if schema not in allowed_schemas:
            continue
        m = MetaData()
        m.reflect(db_engine_sync, schema)
        for table_name in m.sorted_tables[::-1]:
            if table_name.name in prohibited_tables:
                continue
            # noinspection SqlWithoutWhere
            query = text(f'DELETE FROM {table_name} WHERE TRUE;')
            _conn.execute(query)
    _conn.commit()
    _conn.close()


@pytest.fixture(scope='session')
def db_session_factory(db_engine) -> async_sessionmaker:
    return async_sessionmaker(db_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def add_test_users(db_session_factory, db_clean_up) -> None:
    _session = db_session_factory()
    await insert_into_db(_session, 'user_role', test_user_role, 'auth')
    await insert_into_db(_session, 'user_role', test_admin_role, 'auth')
    await insert_into_db(_session, 'user_info', test_user_info, 'auth')
    await insert_into_db(_session, 'user_info', test_admin_info, 'auth')
    await _session.commit()
    await _session.close()


@pytest_asyncio.fixture(scope='function')
async def db_session(db_session_factory) -> AsyncSession:
    db_session_factory: async_sessionmaker
    _ses = db_session_factory()
    try:
        yield _ses
    finally:
        await _ses.close()
