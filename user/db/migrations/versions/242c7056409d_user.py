"""user

Revision ID: 242c7056409d
Revises: 
Create Date: 2023-10-30 20:01:46.094891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '242c7056409d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_profile',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('time_zone', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('avatar_link', sa.String(), nullable=True),
    sa.Column('avatar_status', sa.String(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__user_profile')),
    sa.UniqueConstraint('phone_number', name=op.f('uq__user_profile__phone_number_key')),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('user_profile', schema='user')
    op.drop_table('user_profile', schema='public')
    # ### end Alembic commands ###
