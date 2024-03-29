"""add views to article

Revision ID: 9020864acf2e
Revises: fde9aa91768b
Create Date: 2019-02-15 00:12:04.790222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9020864acf2e'
down_revision = 'fde9aa91768b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('views', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'views')
    # ### end Alembic commands ###
