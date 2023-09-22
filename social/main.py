import uvicorn
from logging import config as logging_config

from async_fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
import sentry_sdk

from api.v1 import rating
from api.v1 import reviews
from api.v1 import bookmarks
from core.config import app_config as config
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

sentry_sdk.init(
    dsn=config.sentry_dsn,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI(
    title=config.api.project_name,
    docs_url='/social_api/api/openapi',
    openapi_url='/social_api/api/openapi.json',
    default_response_class=ORJSONResponse,
)


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return config


root_router = APIRouter(prefix='/social_api/api')
root_router.include_router(rating.router, prefix='/v1/rating', tags=['rating'])
root_router.include_router(reviews.router, prefix='/v1/reviews', tags=['reviews'])
root_router.include_router(bookmarks.router, prefix='/v1/bookmarks', tags=['bookmarks'])
app.include_router(root_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
