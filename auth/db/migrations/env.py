import asyncio
from time import sleep
from typing import Literal
import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, create_engine, schema
from sqlalchemy.engine import Connection
from sqlalchemy.sql.schema import SchemaItem
from sqlalchemy.ext.asyncio import async_engine_from_config

from core.config import app_config
from db.model import metadata

SaSchemaObjType = Literal[
                      "schema",
                      "table",
                      "column",
                      "index",
                      "unique_constraint",
                      "foreign_key_constraint",
                  ],


def include_object(obj: SchemaItem, _: str | None, type_: SaSchemaObjType, *__):
    if type_ == 'table' and obj.schema != app_config.api.db_schema:
        return False
    return True


def include_name(name, type_, _):
    if type_ == "schema":
        return name == app_config.api.db_schema
    else:
        return True


def create_schema_if_not_exists() -> None:
    _engine = create_engine(app_config.postgres_dsn)
    _conn_attempts = 10
    _conn = None

    while _conn_attempts:
        try:
            _conn = _engine.connect()
            break
        except Exception as exc:
            logging.warning('Alembic failed to connect to \'%s\': %s', app_config.postgres_dsn, str(exc))
        sleep(1)
        _conn_attempts -= 1

    if not _engine.dialect.has_schema(_conn, app_config.api.db_schema):
        _conn.execute(schema.CreateSchema(app_config.api.db_schema))
    _conn.commit()
    _conn.close()


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
config.set_main_option(
    "sqlalchemy.url",
    str(app_config.postgres_dsn))

target_metadata = metadata
create_schema_if_not_exists()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_object=include_object,
        include_name=include_name,
        version_table_schema=app_config.api.db_schema
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
