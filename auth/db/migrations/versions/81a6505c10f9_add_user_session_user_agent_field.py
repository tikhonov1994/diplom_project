"""add user_session.user_agent field

Revision ID: 81a6505c10f9
Revises: e09a7998a5b6
Create Date: 2023-08-08 09:42:40.986952

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '81a6505c10f9'
down_revision = 'e09a7998a5b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user_session', sa.Column('user_agent', sa.String(), nullable=True), schema='auth')


def downgrade() -> None:
    op.drop_column('user_session', 'user_agent', schema='auth')
