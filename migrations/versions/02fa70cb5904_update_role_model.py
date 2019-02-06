"""update Role model

Revision ID: 02fa70cb5904
Revises: a55f7caa6596
Create Date: 2019-02-02 16:13:42.940672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02fa70cb5904'
down_revision = 'a55f7caa6596'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permissions')
    op.drop_column('roles', 'default')
    # ### end Alembic commands ###
