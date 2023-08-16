"""add superuser and default roles

Revision ID: 7998e07da9a4
Revises: 81a6505c10f9
Create Date: 2023-08-08 09:54:22.593608

"""
from uuid import uuid4

from alembic import op
from core.config import app_config
from services.utils import generate_hashed_password

# revision identifiers, used by Alembic.
revision = '7998e07da9a4'
down_revision = '81a6505c10f9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    admin_role_id = uuid4()
    admin_password = generate_hashed_password(app_config.api.admin_password)
    op.execute(f'INSERT INTO auth.user_role (id, name) '
               f'VALUES (\'{admin_role_id}\', \'{app_config.api.admin_user_role}\');')
    op.execute(f'INSERT INTO auth.user_role (id, name) '
               f'VALUES (\'{uuid4()}\', \'{app_config.api.default_user_role}\');')
    op.execute(f'INSERT INTO auth.user_info (id, email, password_hash, user_role_id) '
               f'VALUES (\'{uuid4()}\', \'{app_config.api.admin_email}\', \'{admin_password}\', \'{admin_role_id}\');')


def downgrade() -> None:
    op.execute(f'DELETE FROM auth.user_info WHERE email = \'{app_config.api.admin_email}\';')
    op.execute(f'DELETE FROM auth.user_role WHERE name IN (\'admin\', \'{app_config.api.default_user_role}\');')
