import uvicorn
import sentry_sdk

from async_fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from api.v1 import view
from core.config import app_config as config
from core.middleware import LoggingMiddleware

if config.export_logs:
    sentry_sdk.init(
        dsn=config.sentry.dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )

app = FastAPI(
    title=config.api.project_name,
    docs_url='/ugc_api/api/openapi',
    openapi_url='/ugc_api/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.middleware('http')(LoggingMiddleware())


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return config


root_router = APIRouter(prefix='/ugc_api/api')
root_router.include_router(view.router, prefix='/v1/views', tags=['views'])
app.include_router(root_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
