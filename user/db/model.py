from uuid import UUID, uuid4

from core.config import app_config
from sqlalchemy import MetaData
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


class IdMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class UserProfile(Base, IdMixin):
    __tablename__ = 'user_profile'

    email: Mapped[str] = mapped_column(unique=True)
    time_zone: Mapped[str] = mapped_column()
    phone_number: Mapped[int] = mapped_column(unique=True)
    avatar_link: Mapped[str] = mapped_column(nullable=True)
    avatar_status: Mapped[str] = mapped_column(nullable=True)
