from enum import Enum, auto
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM

from db.models import BaseWithId


class UserSessionType(str, Enum):
    NATIVE = auto()
    ...


UserSessionTypeEnum: ENUM = ENUM(
    UserSessionType,
    name="user_session_type",
    create_constraint=True,
    metadata=BaseWithId.metadata,
    validate_strings=True,
)


class UserSession(BaseWithId):
    __tablename__ = 'user_session'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    refresh_token: Mapped[str]
    session_type = mapped_column(UserSessionTypeEnum)
