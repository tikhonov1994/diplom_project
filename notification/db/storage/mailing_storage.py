from datetime import datetime
from uuid import UUID
from db.postgres_connection import DbSessionDep
from sqlalchemy.exc import IntegrityError
from db.models import Mailing
from schemas.mailing import CreateMailingRequestSchema, MailingStatusEnum
from db.storage.exceptions import ItemNotFoundException


class MailingStorage:
    TABLE_NAME = 'mailing'

    def __init__(self, session: DbSessionDep):
        self._session = session

    async def add(self, data: CreateMailingRequestSchema, recipients_list: list) -> None:
        model = Mailing(subject=data.subject, receiver_ids=recipients_list, template_id=data.template_id,
                        template_params=data.template_params, status=MailingStatusEnum.created,
                        created_at=datetime.now(), updated_at=datetime.now())
        try:
            self._session.add(model)
            await self._session.flush()
            await self._session.refresh(model)

            return model.id
        except IntegrityError as e:
            print('tuyttt?')
            print(e)
            self._session.rollback()

    async def update_status(self, mailing_id: UUID, status: str) -> None:
        if mailing := await self._session.get(mailing_id):
            mailing.status = status
            await self._session.flush(mailing)
        else:
            raise ItemNotFoundException(mailing_id, self.TABLE_NAME)
