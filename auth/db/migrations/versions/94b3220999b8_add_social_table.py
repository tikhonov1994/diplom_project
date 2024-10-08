"""add social table

Revision ID: 94b3220999b8
Revises: a6ab8d85f09e
Create Date: 2023-08-22 15:26:14.009883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94b3220999b8'
down_revision = 'a6ab8d85f09e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_social',
    sa.Column('user_info_id', sa.Uuid(), nullable=False),
    sa.Column('social_name', sa.String(), nullable=False),
    sa.Column('social_id', sa.String(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['user_info_id'], ['auth.user_info.id'], name=op.f('fk__user_social__user_info_id__user_info'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__user_social')),
    sa.UniqueConstraint('social_name', 'social_id', name='_name_id_uc'),
    schema='auth'
    )
    op.drop_constraint('fk__user_info__user_role_id__user_role', 'user_info', schema='auth', type_='foreignkey')
    op.create_foreign_key(op.f('fk__user_info__user_role_id__user_role'), 'user_info', 'user_role', ['user_role_id'], ['id'], source_schema='auth', referent_schema='auth', ondelete='CASCADE')
    op.drop_constraint('fk__user_session__user_info_id__user_info', 'user_session', schema='auth', type_='foreignkey')
    op.create_foreign_key(op.f('fk__user_session__user_info_id__user_info'), 'user_session', 'user_info', ['user_info_id'], ['id'], source_schema='auth', referent_schema='auth', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk__user_session__user_info_id__user_info'), 'user_session', schema='auth', type_='foreignkey')
    op.create_foreign_key('fk__user_session__user_info_id__user_info', 'user_session', 'user_info', ['user_info_id'], ['id'], source_schema='auth', referent_schema='auth')
    op.drop_constraint(op.f('fk__user_info__user_role_id__user_role'), 'user_info', schema='auth', type_='foreignkey')
    op.create_foreign_key('fk__user_info__user_role_id__user_role', 'user_info', 'user_role', ['user_role_id'], ['id'], source_schema='auth', referent_schema='auth')
    op.drop_table('user_social', schema='auth')
    # ### end Alembic commands ###
