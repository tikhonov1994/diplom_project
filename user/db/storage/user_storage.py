from typing import Annotated

from fastapi import Depends

from db.storage.generic_storage import GenericStorageMixin
from db.storage import DbSessionDep
from db.model import UserProfile


class UserStorage(GenericStorageMixin[UserProfile]):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserProfile, session)
        self._session = session


UserStorageDep = Annotated[UserStorage, Depends()]
