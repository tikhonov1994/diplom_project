from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
import sentry_sdk

from api.websocket import router as ws_router
from core.config import app_config as cfg
from core.middleware import LoggingMiddleware
from core.logger import get_logger
from handlers.mailing import rabbitmq_consumer_task

logger = get_logger()

if cfg.export_logs:
    sentry_sdk.init(
        dsn=cfg.sentry_dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with rabbitmq_consumer_task() as task:
        await task()
        yield


app = FastAPI(lifespan=lifespan)
app.middleware('http')(LoggingMiddleware())
app.include_router(ws_router)

if __name__ == '__main__':
    logger.info('%s is up and running at %s:%d.',
                cfg.ws.project_name,
                cfg.ws.host,
                cfg.ws.port)
    uvicorn.run(
        'main:app',
        host=cfg.ws.host,
        port=cfg.ws.port,
    )
