from typing import Annotated  # type: ignore[attr-defined]
from db.storage.notification_storage import NotificationStorage
from fastapi import Depends

NotificationStorageDep = Annotated[NotificationStorage, Depends()]


__all__ = []
