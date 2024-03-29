"""empty message

Revision ID: 3e3854805b4e
Revises: 2d2e53609964
Create Date: 2019-03-02 11:48:07.349692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e3854805b4e'
down_revision = '2d2e53609964'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('replys',
    sa.Column('replyer_id', sa.Integer(), nullable=False),
    sa.Column('replyed_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['replyed_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['replyer_id'], ['comments.id'], ),
    sa.PrimaryKeyConstraint('replyer_id', 'replyed_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('replys')
    # ### end Alembic commands ###
