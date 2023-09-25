from logging import config as logging_config

import uvicorn
from async_fastapi_jwt_auth import AuthJWT
from core.config import app_config as config
from core.logger import LOGGING
from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import bookmarks, rating, reviews

logging_config.dictConfig(LOGGING)

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
