from uuid import uuid4
from contextlib import closing

import typer
from pydantic import ValidationError
from sqlalchemy import create_engine, Connection, text
from sqlalchemy.exc import IntegrityError

from schemas.auth import LoginSchema
from core.config import app_config
from services.utils import generate_hashed_password

app = typer.Typer()


@app.command()
def create_superuser(email: str, password):
    try:
        validated_creds = LoginSchema(email=email, password=password)
        password_hash = generate_hashed_password(validated_creds.password)

        engine = create_engine(url=app_config.postgres_dsn)
        with closing(engine.connect()) as connection:
            connection: Connection

            get_admin_role_stmt = text(f'SELECT id FROM {app_config.api.db_schema}.user_role '
                                       f'WHERE name = \'{app_config.api.admin_user_role}\';')
            admin_role_id = connection.execute(get_admin_role_stmt).scalar()

            su_stmt = text(f'INSERT INTO {app_config.api.db_schema}.user_info (id, email, password_hash, user_role_id) '
                           f'VALUES (\'{uuid4()}\', \'{email}\', \'{password_hash}\', \'{admin_role_id}\');')
            _ = connection.execute(su_stmt)
            connection.commit()
    except ValidationError as err:
        print('Email is invalid')
    except IntegrityError as err:
        print('The email is already in use')


if __name__ == "__main__":
    app()
