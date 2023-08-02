import os
import hashlib

from typing import Annotated

from fastapi import Depends
from db.model import User
from db.storage import DbSessionDep
from db.storage.generic_storage import GenericStorage, GenericStorageException

from sqlalchemy import select


class UserEmailNotFoundException(GenericStorageException):
    def __init__(self, email: str) -> None:
        super().__init__()
        self._instance_email = email

    def __repr__(self) -> str:
        return f'User with email: \'{self._instance_email}\' not found'


class UserService:

    def __init__(self, storage: DbSessionDep) -> None:
        super().__init__(storage)

    async def get_user_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        if result := await self._session.execute(stmt).first():
            return result
        raise UserEmailNotFoundException(item_type=User, email=email)

    @staticmethod
    def generate_hashed_password(password: str):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        return key + salt

    @staticmethod
    def check_password(pass_to_check: str, user: User):
        password = user.password_hash
        salt = password[-32:]
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            pass_to_check.encode('utf-8'), # Конвертирование пароля в байты
            salt, 
            100000
        )
        if new_key == password:
            return True
        else:
            return False


UserServiceDep = Annotated[UserService, Depends()]
