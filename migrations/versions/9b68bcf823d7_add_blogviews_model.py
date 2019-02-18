"""add blogviews model

Revision ID: 9b68bcf823d7
Revises: 9020864acf2e
Create Date: 2019-02-16 13:56:48.404325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b68bcf823d7'
down_revision = '9020864acf2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blogviews')
    # ### end Alembic commands ###