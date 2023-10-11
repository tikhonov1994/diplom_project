from uuid import UUID
from db.rabbit_connection import rabbit_connection
from db.storage import MailingStorageDep, TemplateStorageDep
from schemas.mailing import CreateMailingRequestSchema, MailingMessageSchema


class MailingService:
    BATCH_SIZE = 1000

    def __init__(self, mailing_storage: MailingStorageDep, template_storge: TemplateStorageDep):
        self._mailing_storage = mailing_storage
        self._template_storge = template_storge

    async def handle(self, data: CreateMailingRequestSchema) -> None:
        length = len(data.recipients_list)
        for idx in range(0, length, self.BATCH_SIZE):
            batched_recipients_list = data.recipients_list[idx:min(idx + self.BATCH_SIZE, length)]

            mailing_id = await self._mailing_storage.add(data, batched_recipients_list)

            message_data = MailingMessageSchema(
                mailing_id=str(mailing_id), subject=data.subject, template_id=str(data.template_id),
                recipients_list=[str(item) for item in batched_recipients_list], template_params=data.template_params
            )

            await rabbit_connection.send_messages(
                message_data
            )

    async def get_registration_mailing_data(self, user_id: UUID, email: str):
        template_name = 'registration'
        template = await self._template_storge.get_by_name(template_name)
        template_params = {
            'email': email,
        }
        subject = 'Welcome!'

        return CreateMailingRequestSchema(
            recipients_list=[user_id], subject=subject, template_id=template.id, template_params=template_params,
        )

    async def update_status(self, mailing_id: UUID, status: str):
        await self._mailing_storage.update_status(mailing_id, status)

