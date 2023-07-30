import uvicorn
from logging import config as logging_config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy import create_engine

from core.config import app_config as config
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


engine = create_engine(
    'postgresql+%s://%s:%s@%s:%s/%s' % (
        config.postgres_driver, config.postgres_user, config.postgres_password,
        config.postgres_host, config.postgres_port, config.postgres_db
    )
)


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
