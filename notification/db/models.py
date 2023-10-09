from typing import Any
from uuid import uuid4, UUID

from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.dialects.postgresql import JSONB

from core.config import app_config
from sqlalchemy import ForeignKey, MetaData, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


name_convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s_key',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}


print(app_config.api.db_schema)
metadata = MetaData(naming_convention=name_convention, schema=app_config.api.db_schema)


class Base(DeclarativeBase):
    metadata = metadata
    type_annotation_map = {
        dict[str, Any]: JSONB,
        list[str]: ARRAY(String),
    }


class IdMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class Notification(Base, IdMixin):
    __tablename__ = 'notification'

    subject: Mapped[str]
    receiver_ids: Mapped[list[str]]
    template_id: Mapped[UUID]
    template_params: Mapped[dict[str, Any]]

