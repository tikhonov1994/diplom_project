import asyncio

import sentry_sdk

from adapters.rabbitmq import ConfiguredRabbitmq
from core.config import app_config
from core.logger import get_logger
from handlers import sender_type

if app_config.export_logs:
    sentry_sdk.init(
        dsn=app_config.sentry_dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1
    )


async def main() -> None:
    logger = get_logger()
    rabbitmq = ConfiguredRabbitmq()
    await rabbitmq.configure_broker()

    async with rabbitmq.get_configured_channel() as channel:
        message_queue = await channel.get_queue(app_config.worker.queue_name)
        logger.info('Connected to %s, ready to handle messages!', app_config.rabbitmq.dsn)

        try:
            await message_queue.consume(sender_type().process_message)
        except Exception as exc:
            if app_config.export_logs:
                sentry_sdk.capture_exception(exc)
            else:
                raise exc

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
