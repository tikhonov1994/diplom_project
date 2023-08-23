from datetime import datetime
from uuid import UUID, uuid4

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

metadata = MetaData(naming_convention=name_convention, schema=app_config.api.db_schema)


class Base(DeclarativeBase):
    metadata = metadata


class IdMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class UserInfo(Base, IdMixin):
    __tablename__ = 'user_info'

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    user_role_id: Mapped[UUID] = mapped_column(ForeignKey('user_role.id', ondelete="CASCADE"))

    role: Mapped['UserRole'] = relationship(lazy='joined')
    active_sessions: Mapped['UserSession'] = relationship(lazy='joined', cascade="all, delete",
                                                          passive_deletes=True)
    socials: Mapped['UserSocial'] = relationship(lazy='joined', cascade="all, delete",
                                                 passive_deletes=True)


class UserSession(Base, IdMixin):
    __tablename__ = 'user_session'

    user_info_id: Mapped[UUID] = mapped_column(ForeignKey('user_info.id', ondelete="CASCADE"))
    user_agent: Mapped[str] = mapped_column(nullable=False)
    refresh_token_jti: Mapped[str]
    start_at: Mapped[datetime]
    end_at: Mapped[datetime] = mapped_column(nullable=True)


class UserRole(Base, IdMixin):
    __tablename__ = 'user_role'

    name: Mapped[str] = mapped_column(unique=True)


class UserSocial(Base, IdMixin):
    __tablename__ = 'user_social'

    user_info_id: Mapped[UUID] = mapped_column(ForeignKey('user_info.id', ondelete="CASCADE"))
    social_name: Mapped[str]
    social_id: Mapped[str]

    __table_args__ = (UniqueConstraint('social_name', 'social_id', name='_name_id_uc'),)
