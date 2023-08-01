from sqlalchemy.orm import Mapped, relationship

from db.models import BaseWithId
from db.models.UserSession import UserSession


class User(BaseWithId):
    __tablename__ = 'UserInfo'

    email: Mapped[str]
    password_hash: Mapped[str]
    active_sessions: Mapped[UserSession] = relationship()
