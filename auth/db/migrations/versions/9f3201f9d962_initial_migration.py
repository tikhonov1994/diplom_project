"""initial migration

Revision ID: 9f3201f9d962
Revises: 
Create Date: 2023-08-02 00:09:57.827661

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9f3201f9d962'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_role',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__user_role')),
                    schema='auth'
                    )
    op.create_table('user_info',
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password_hash', sa.String(), nullable=False),
                    sa.Column('user_role_id', sa.Uuid(), nullable=False),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.ForeignKeyConstraint(['user_role_id'], ['auth.user_role.id'],
                                            name=op.f('fk__user_info__user_role_id__user_role')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__user_info')),
                    sa.UniqueConstraint('email', name=op.f('uq__user_info__email_key')),
                    schema='auth'
                    )
    op.create_table('user_session',
                    sa.Column('user_info_id', sa.Uuid(), nullable=False),
                    sa.Column('refresh_token', sa.String(), nullable=False),
                    sa.Column('session_type',
                              sa.Enum('NATIVE', name='usersessiontype', schema='auth', inherit_schema=True),
                              nullable=True),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.ForeignKeyConstraint(['user_info_id'], ['auth.user_info.id'],
                                            name=op.f('fk__user_session__user_info_id__user_info')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__user_session')),
                    schema='auth'
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_session', schema='auth')
    op.drop_table('user_info', schema='auth')
    op.drop_table('user_role', schema='auth')
    # ### end Alembic commands ###
