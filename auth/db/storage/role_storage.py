from db.storage.generic_storage import GenericStorageMixin
from db.storage.session import DbSessionDep
from db.model import UserRole


class RoleStorage(GenericStorageMixin):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserRole, session)
        self._session = session
