from enum import Enum, auto
from uuid import UUID, uuid4

from sqlalchemy import MetaData, ForeignKey
from sqlalchemy import Enum as SaEnum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.config import app_config

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


class UserInfo(Base, IdMixin):
    __tablename__ = 'user_info'

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    user_role_id: Mapped[UUID] = mapped_column(ForeignKey('user_role.id'))

    role: Mapped['UserRole'] = relationship()
    active_sessions: Mapped['UserSession'] = relationship()


class UserSessionType(str, Enum):
    NATIVE = auto()
    ...


class UserSession(Base, IdMixin):
    __tablename__ = 'user_session'

    user_info_id: Mapped[UUID] = mapped_column(ForeignKey('user_info.id'))
    refresh_token: Mapped[str]
    session_type = mapped_column(SaEnum(UserSessionType, inherit_schema=True))
    user_agent: Mapped[str] = mapped_column(nullable=True)


class UserRole(Base, IdMixin):
    __tablename__ = 'user_role'

    name: Mapped[str] = mapped_column(unique=True)
