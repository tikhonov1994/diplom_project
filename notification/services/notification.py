import uuid

from db.rabbit_connection import rabbit_connection
from db.storage import NotificationStorageDep
from schemas.notification import NotificationRequestSchema, NotificationMessageSchema


class NotificationService:
    BATCH_SIZE = 1000

    def __init__(self, storage: NotificationStorageDep):
        self._storage = storage

    async def handle(self, data: NotificationRequestSchema):
        length = len(data.recipients_list)
        for idx in range(0, length, self.BATCH_SIZE):
            batched_recipients_list = data.recipients_list[idx:min(idx + self.BATCH_SIZE, length)]
            notification_id = await self._storage.add(data, batched_recipients_list)

            message_data = NotificationMessageSchema(
                notification_id=str(notification_id), subject=data.subject, template_id=str(data.template_id),
                recipients_list=[str(item) for item in batched_recipients_list], template_params=data.template_params
            )

            await rabbit_connection.send_messages(
                message_data
                # delay=20
            )
