import uuid
from typing import Any
from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import String, ARRAY, Uuid
from sqlalchemy.dialects.postgresql import JSONB

from core.config import app_config
from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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


metadata = MetaData(naming_convention=name_convention, schema=app_config.api.db_schema)


class Base(DeclarativeBase):
    metadata = metadata
    type_annotation_map = {
        dict[str, Any]: JSONB,
        list[str]: ARRAY(String),
        list[uuid]: ARRAY(Uuid),
    }


class IdMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class Mailing(Base, IdMixin):
    __tablename__ = 'mailing'

    subject: Mapped[str]
    status: Mapped[str]
    receiver_ids: Mapped[list[uuid]]
    template_id: Mapped[UUID] = mapped_column(ForeignKey('template.id', ondelete="CASCADE"))
    template_params: Mapped[dict[str, Any]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]


class Template(Base, IdMixin):
    __tablename__ = 'template'

    name: Mapped[str]
    html_template: Mapped[UUID]
    attributes: Mapped[dict[str, Any]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

