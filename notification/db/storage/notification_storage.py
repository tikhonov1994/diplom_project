from sqlalchemy import select

from db.postgres_connection import DbSessionDep
# from utils.tracer import sub_span todo
from sqlalchemy.exc import IntegrityError
from db.models import Notification
from schemas.notification import NotificationRequestSchema


class NotificationStorage:
    def __init__(self, session: DbSessionDep) -> str:
        self._session = session

    async def add(self, data: NotificationRequestSchema, recipients_list: list) -> None:
        model = Notification(subject=data.subject, receiver_ids=recipients_list, template_id=data.template_id,
                             template_params=data.template_params)
        try:
            self._session.add(model)
            await self._session.flush()
            await self._session.refresh(model)

            return model.id
        except IntegrityError as e:
            print(e)
            self._session.rollback()
