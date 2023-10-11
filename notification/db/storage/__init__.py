from typing import Annotated  # type: ignore[attr-defined]
from db.storage.mailing_storage import MailingStorage
from db.storage.template_storage import TemplateStorage
from fastapi import Depends

MailingStorageDep = Annotated[MailingStorage, Depends()]
TemplateStorageDep = Annotated[TemplateStorage, Depends()]


__all__ = [
    'MailingStorageDep',
    'TemplateStorageDep'
]
