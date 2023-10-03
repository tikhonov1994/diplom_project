import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
import sentry_sdk

from api.v1 import notification
from core.config import app_config as config
from core.middleware import LoggingMiddleware

if config.export_logs:
    sentry_sdk.init(
        dsn=config.sentry_dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )

app = FastAPI(
    title=config.api.project_name,
    docs_url='/notification_api/api/openapi',
    openapi_url='/notification_api/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.middleware('http')(LoggingMiddleware())


root_router = APIRouter(prefix='/notification_api/api')
root_router.include_router(notification.router, prefix='/v1/notification', tags=['notification'])
app.include_router(root_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
