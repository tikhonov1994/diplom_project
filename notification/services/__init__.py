from typing import Annotated  # type: ignore[attr-defined]

from fastapi import Depends
from services.notification import NotificationService

NotificationServiceDep = Annotated[NotificationService, Depends()]

__all__ = ['NotificationServiceDep',]
