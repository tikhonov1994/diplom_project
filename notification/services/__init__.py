from typing import Annotated  # type: ignore[attr-defined]

from fastapi import Depends
from services.mailing import MailingService

MailingServiceDep = Annotated[MailingService, Depends()]

__all__ = ['MailingServiceDep',]
