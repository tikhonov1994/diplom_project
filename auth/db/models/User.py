from sqlalchemy.orm import Mapped

from db.models import BaseWithId


class User(BaseWithId):
    __tablename__ = 'UserInfo'

    email: Mapped[str]
    password_hash: Mapped[str]
