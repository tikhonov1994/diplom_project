import asyncio
import json
from uuid import UUID

import aio_pika
import jinja2
import aiosmtplib as smtp
from email.message import EmailMessage

from handlers.consumer_base import EmailConsumerBase
from rabbitmq import connect
from core.logger import logger
from core.config import app_config as cfg
from schemas.mailing import MailingSchema
from schemas.notification import MailTemplateSchema
from schemas.auth import UserInfoSchema
from adapters import AuthServiceAdapter, NotificationServiceAdapter


class SimpleEmailConsumer(EmailConsumerBase):
    @classmethod
    async def process_message(cls, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process(ignore_processed=True, requeue=False), \
                AuthServiceAdapter() as auth_adapter, \
                NotificationServiceAdapter() as notification_adapter:
            logger.debug('New mailing [%s]: %s', message.message_id, message.body.decode())
            mailing = MailingSchema.model_validate(json.loads(message.body.decode()))
            delivered_to: set[UUID] = set()

            try:
                template_info: MailTemplateSchema = await notification_adapter.get_mail_template(mailing.template_id)
                template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(template_info.body)
                smtp_client = smtp.SMTP(**cfg.worker.smtp_connect_params)
                await smtp_client.connect()
                await smtp_client.starttls()

                for recipient_id in mailing.recipients_list:
                    recipient: UserInfoSchema = await auth_adapter.get_user_info(recipient_id)
                    email_body = template.render(mailing.template_params | recipient.template_params)
                    await cls._send_rendered_email(smtp_client, recipient.email, mailing.subject, email_body)
                    delivered_to.add(recipient_id)
            except Exception as exc:
                mailing.recipients_list.difference_update(delivered_to)
                logger.error('Requeuing mailing [%s] after 1 second due to unhandled exception: %s.',
                             message.message_id, str(exc))
                await asyncio.sleep(1.)
                _conn = await connect()
                _channel = await _conn.channel()
                await _channel.default_exchange.publish(
                    aio_pika.Message(mailing.model_dump_json().encode()),
                    routing_key=message.routing_key
                )
            else:
                await message.ack()
            finally:
                smtp_client.close()

    @staticmethod
    async def _send_rendered_email(client: smtp.SMTP,
                                   recipient_email: str,
                                   subject: str,
                                   body: str) -> None:
        message = EmailMessage()
        message['From'] = cfg.worker.email_address
        message['To'] = recipient_email
        message['Subject'] = subject
        message.add_alternative(body, subtype='html')
        await client.send_message(message)
