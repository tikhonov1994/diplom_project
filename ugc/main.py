import uvicorn
from logging import config as logging_config
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from api.v1 import view
from core.config import app_config as config
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


app = FastAPI(
    title=config.api.project_name,
    docs_url='/ugc_api/api/openapi',
    openapi_url='/ugc_api/api/openapi.json',
    default_response_class=ORJSONResponse,
)

root_router = APIRouter(prefix='/ugc_api/api')
root_router.include_router(view.router, prefix='/v1/views', tags=['views'])
app.include_router(root_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
