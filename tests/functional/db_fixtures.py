import pytest
import pytest_asyncio
from functional.test_data.db_data import (test_admin_info, test_admin_role, test_notification_register_template,
                                          test_user_info, test_user_role, test_notification_template)
from functional.test_data.user_data import test_user_profile
from functional.utils.db import insert_into_db
from settings import test_settings as config
from sqlalchemy import Engine, MetaData, create_engine, inspect, text, Connection
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)


@pytest_asyncio.fixture(scope='session')
async def db_engine() -> AsyncEngine:
    engine = create_async_engine(config.postgres_dsn, future=True)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def secure_db_engine() -> AsyncEngine:
    engine = create_async_engine(config.secure_postgres_dsn, future=True)
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


@pytest.fixture(scope='session')
def secure_db_engine_sync() -> Engine:
    engine = create_engine(config.secure_postgres_dsn, future=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope='session', autouse=True)
def db_clean_up(db_engine_sync, secure_db_engine_sync) -> None:
    db_engine_sync: Engine
    secure_db_engine_sync: Engine
    _conn = db_engine_sync.connect()
    _sec_conn = secure_db_engine_sync.connect()

    def _clean_up(engine: Engine, conn: Connection) -> None:
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()

        allowed_schemas = ['public',
                           'content',
                           config.auth_db_schema,
                           config.notification_db_schema,
                           config.user_db_schema]

        prohibited_tables = ['alembic_version']

        for schema in schemas:
            if schema not in allowed_schemas:
                continue
            m = MetaData()
            m.reflect(engine, schema)
            for table_name in m.sorted_tables[::-1]:
                if table_name.name in prohibited_tables:
                    continue
                # noinspection SqlWithoutWhere
                query = text(f'DELETE FROM {table_name} WHERE TRUE;')
                conn.execute(query)
        conn.commit()
        conn.close()

    _clean_up(db_engine_sync, _conn)
    _clean_up(secure_db_engine_sync, _sec_conn)


@pytest.fixture(scope='session')
def db_session_factory(db_engine) -> async_sessionmaker:
    return async_sessionmaker(db_engine, expire_on_commit=False)


@pytest.fixture(scope='session')
def secure_db_session_factory(secure_db_engine) -> async_sessionmaker:
    return async_sessionmaker(secure_db_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def add_test_users(db_session_factory, secure_db_session_factory, db_clean_up) -> None:
    _session = db_session_factory()
    await insert_into_db(_session, 'user_role', test_user_role, 'auth')
    await insert_into_db(_session, 'user_role', test_admin_role, 'auth')
    await insert_into_db(_session, 'user_info', test_user_info, 'auth')
    await insert_into_db(_session, 'user_info', test_admin_info, 'auth')
    await _session.commit()
    await _session.close()

    _sec_session = secure_db_session_factory()
    await insert_into_db(_sec_session, 'user_profile', test_user_profile, 'public')
    await _sec_session.commit()
    await _sec_session.close()


@pytest_asyncio.fixture(scope='function')
async def db_session(db_session_factory) -> AsyncSession:
    db_session_factory: async_sessionmaker
    _ses = db_session_factory()
    try:
        yield _ses
    finally:
        await _ses.close()


@pytest_asyncio.fixture(scope='function')
async def secure_db_session(secure_db_session_factory) -> AsyncSession:
    secure_db_session_factory: async_sessionmaker
    _ses = secure_db_session_factory()
    try:
        yield _ses
    finally:
        await _ses.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_notification_schema(db_session_factory, db_clean_up) -> None:
    _session = db_session_factory()

    queries = [
        text('CREATE SCHEMA IF NOT EXISTS notification;'),
        text("""CREATE TABLE IF NOT EXISTS notification.mailing (
            id uuid NOT NULL,
            receiver_ids uuid[] NOT NULL,
            status character varying(50) NOT NULL,
            subject character varying(255) NOT NULL,
            template_params jsonb NOT NULL,
            created_at timestamp with time zone NOT NULL,
            updated_at timestamp with time zone NOT NULL,
            template_id uuid NOT NULL
        );"""),
        text("""CREATE TABLE IF NOT EXISTS notification.template (
                id uuid NOT NULL,
                name character varying(64) NOT NULL,
                html_template text NOT NULL,
                attributes jsonb NOT NULL
        );"""),
    ]
    for query in queries:
        await _session.execute(query)
    await _session.commit()


@pytest_asyncio.fixture(scope='session')
async def add_test_template(db_session_factory, db_clean_up) -> None:
    _session = db_session_factory()
    await insert_into_db(_session, 'template', test_notification_template, 'notification')
    await _session.commit()
    await _session.close()


@pytest_asyncio.fixture(scope='session')
async def add_register_template(db_session_factory, db_clean_up) -> None:
    _session = db_session_factory()
    await insert_into_db(_session, 'template', test_notification_register_template, 'notification')
    await _session.commit()
    await _session.close()
