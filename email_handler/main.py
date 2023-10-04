import asyncio
import sentry_sdk

from rabbitmq import connect
from core.config import app_config
from core.logger import logger
from handlers import sender_type

if app_config.export_logs:
    sentry_sdk.init(
        dsn=app_config.sentry_dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1
    )


async def main() -> None:
    logger.info('Connecting to %s...', app_config.rabbitmq.dsn)
    connection = await connect()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=app_config.worker.prefetch_count)
    queue = await channel.declare_queue(app_config.worker.queue_name, auto_delete=True)
    logger.debug('Worker subscribed on queue: \'%s\'', app_config.worker.queue_name)
    logger.debug('Set prefetch count to %d', app_config.worker.prefetch_count)
    logger.info('Connected, ready to handle messages!')

    try:
        await queue.consume(sender_type().process_message)
    except Exception as exc:
        sentry_sdk.capture_exception(exc)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
