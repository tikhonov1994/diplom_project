import asyncio
import sys
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
import sentry_sdk

from core.config import app_config as config
from core.middleware import LoggingMiddleware
from api.v1.images import router as images_router

if config.export_logs:
    sentry_sdk.init(
        dsn=config.sentry_dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )

app = FastAPI(
    title=config.api.project_name,
    docs_url='/user_api/api/openapi',
    openapi_url='/user_api/api/openapi.json',
    default_response_class=ORJSONResponse,
)

if not config.debug:
    app.middleware('http')(LoggingMiddleware())

root_router = APIRouter(prefix='/user_api/api/v1')
root_router.include_router(images_router, prefix='/images', tags=['images'])
# insert: root_router.include_router(...) here.
# ...
app.include_router(root_router)

if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
