import uvicorn
from logging import config as logging_config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy import create_engine

from core.config import app_config as config
from core.logger import LOGGING
from api.v1 import users, roles
from auth.user import router as user_router

logging_config.dictConfig(LOGGING)

engine = create_engine(
    'postgresql+%s://%s:%s@%s:%s/%s' % (
        config.postgres_driver, config.postgres_user, config.postgres_password,
        config.postgres_host, config.postgres_port, config.postgres_db
    )
)

app = FastAPI(
    title=config.api.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
app.include_router(roles.router, prefix='/api/v1/roles', tags=['roles'])
app.include_router(user_router, prefix='/auth', tags=['users'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
    )
