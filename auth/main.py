import uvicorn
from logging import config as logging_config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import app_config as config
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


app = FastAPI(
    title=config.api.project_name,
    docs_url='/auth/openapi',
    openapi_url='/auth/openapi.json',
    default_response_class=ORJSONResponse,
)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
