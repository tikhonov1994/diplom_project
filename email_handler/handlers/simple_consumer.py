import asyncio
import json
from uuid import UUID

import aio_pika
import jinja2
import aiosmtplib as smtp
from email.message import EmailMessage

from handlers.consumer_base import EmailConsumerBase
from adapters.rabbitmq import ConfiguredRabbitmq
from core.logger import get_logger
from core.config import app_config as cfg
from schemas.mailing import MailingSchema, MailingStatusEnum
from schemas.notification import MailTemplateSchema
from schemas.auth import UserInfoSchema
from adapters import AuthServiceAdapter, AdminServiceAdapter, NotificationServiceAdapter


class SimpleEmailConsumer(EmailConsumerBase):
    _RETRY_INTERVAL_SEC = 1.
    _RETRY_COUNT = 5

    @classmethod
    async def process_message(cls, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process(ignore_processed=True, requeue=False), \
                AuthServiceAdapter() as auth_adapter, \
                AdminServiceAdapter() as admin_adapter, \
                NotificationServiceAdapter() as notify_adapter:
            mailing = MailingSchema.model_validate(json.loads(message.body.decode()))
            logger = get_logger(mailing.request_id)
            logger.debug('New mailing [%s]: %s', message.message_id, message.body.decode())
            delivered_to: set[UUID] = set()
            try:
                template_info: MailTemplateSchema = await admin_adapter.get_mail_template(mailing.template_id)
                template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(template_info.body)
                smtp_client = await cls._get_smtp_client()

                for recipient_id in mailing.recipients_list:
                    recipient: UserInfoSchema = await auth_adapter.get_user_info(recipient_id)
                    email_body = template.render(mailing.template_params | recipient.template_params)
                    await cls._send_rendered_email(smtp_client, recipient.email, mailing.subject, email_body)
                    delivered_to.add(recipient_id)
            except Exception as exc:
                if mailing.retries_cnt > cls._RETRY_COUNT:
                    logger.error('Failed to perform mailing [%s] after %d attempts.',
                                 mailing.mailing_id, cls._RETRY_COUNT)
                    await cls._requeue(mailing, routing_key=cfg.worker.dl_routing_key)
                    await notify_adapter.post_mailing_status(
                        request_id=mailing.request_id,
                        mailing_id=mailing.mailing_id,
                        mailing_status=MailingStatusEnum.failed
                    )
                mailing.retries_cnt += 1
                mailing.recipients_list.difference_update(delivered_to)
                logger.error('Requeuing mailing [%s] after %f second(s) due to unhandled exception: %s.',
                             mailing.mailing_id, str(exc), cls._RETRY_INTERVAL_SEC)
                await asyncio.sleep(cls._RETRY_INTERVAL_SEC)
                await cls._requeue(mailing, routing_key=cfg.worker.routing_key)
            else:
                await message.ack()
                await notify_adapter.post_mailing_status(
                    request_id=mailing.request_id,
                    mailing_id=mailing.mailing_id,
                    mailing_status=MailingStatusEnum.done
                )
            finally:
                smtp_client.close()

    @staticmethod
    async def _get_smtp_client() -> smtp.SMTP:
        smtp_client = smtp.SMTP(**cfg.worker.smtp_connect_params)
        await smtp_client.connect()
        if cfg.worker.smtp_use_tls:
            await smtp_client.starttls()
        return smtp_client

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

    @staticmethod
    async def _requeue(mailing: MailingSchema, routing_key: str) -> None:
        async with ConfiguredRabbitmq().get_configured_channel() as channel:  # type: aio_pika.abc.AbstractChannel
            _exchange = await channel.get_exchange(cfg.worker.exchange_name)
            await _exchange.publish(
                aio_pika.Message(mailing.model_dump_json().encode()),
                routing_key=routing_key
            )
