"""add superuser and default roles

Revision ID: 7998e07da9a4
Revises: 81a6505c10f9
Create Date: 2023-08-08 09:54:22.593608

"""
from uuid import uuid4

from alembic import op

from core.config import app_config
from services.utils import UtilService

# revision identifiers, used by Alembic.
revision = '7998e07da9a4'
down_revision = '81a6505c10f9'
branch_labels = None
depends_on = None


def get_superuser_password() -> tuple[str, str]:
    hashed_su_password = UtilService().generate_hashed_password(app_config.api.admin_password)
    return '\\x' + hashed_su_password.hex()


def upgrade() -> None:
    admin_role_id = uuid4()
    admin_password = get_superuser_password()
    op.execute(f'INSERT INTO auth.user_role (id, name) VALUES (\'{admin_role_id}\', \'admin\');')
    op.execute(f'INSERT INTO auth.user_role (id, name) VALUES (\'{uuid4()}\', \'registered_user\');')
    op.execute(f'INSERT INTO auth.user_info (id, email, password_hash, user_role_id) '
               f'VALUES (\'{uuid4()}\', \'{app_config.api.admin_email}\', \'{admin_password}\', \'{admin_role_id}\');')


def downgrade() -> None:
    op.execute(f'DELETE FROM auth.user_info WHERE email = \'{app_config.api.admin_email}\';')
    op.execute('DELETE FROM auth.user_role WHERE name IN (\'admin\', \'registered_user\');')
