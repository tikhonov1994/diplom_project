import uvicorn
from async_fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
import sentry_sdk

from api.v1 import rating
from api.v1 import reviews
from api.v1 import bookmarks
from api.v1 import user_grade
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
    docs_url='/social_api/api/openapi',
    openapi_url='/social_api/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.middleware('http')(LoggingMiddleware())


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return config


root_router = APIRouter(prefix='/social_api/api')
root_router.include_router(rating.router, prefix='/v1/rating', tags=['rating'])
root_router.include_router(reviews.router, prefix='/v1/reviews', tags=['reviews'])
root_router.include_router(bookmarks.router, prefix='/v1/bookmarks', tags=['bookmarks'])
root_router.include_router(user_grade.router, prefix='/v1/user_grade', tags=['user_grade'])
app.include_router(root_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
