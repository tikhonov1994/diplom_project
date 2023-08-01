from enum import Enum, auto
from uuid import UUID, uuid4

from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM

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

metadata = MetaData(naming_convention=name_convention)


class Base(DeclarativeBase):
    metadata = metadata


class IdMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class User(Base, IdMixin):
    __tablename__ = 'user_info'

    email: Mapped[str]
    password_hash: Mapped[str]
    active_sessions: Mapped['UserSession'] = relationship()


class UserSessionType(str, Enum):
    NATIVE = auto()
    ...


UserSessionTypeEnum: ENUM = ENUM(
    UserSessionType,
    name="user_session_type",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


class UserSession(Base, IdMixin):
    __tablename__ = 'user_session'

    user_info_id: Mapped[UUID] = mapped_column(ForeignKey('user_info.id'))
    refresh_token: Mapped[str]
    session_type = mapped_column(UserSessionTypeEnum)


__all__ = ['metadata', 'Base', 'IdMixin']
