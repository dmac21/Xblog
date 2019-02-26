"""empty message

Revision ID: e9b176936f86
Revises: 34b38a9d96b9
Create Date: 2019-02-26 22:48:06.963600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9b176936f86'
down_revision = '34b38a9d96b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('article_id', sa.Integer(), nullable=True))
    op.add_column('comments', sa.Column('author_email', sa.String(length=64), nullable=True))
    op.add_column('comments', sa.Column('author_name', sa.String(length=64), nullable=True))
    op.add_column('comments', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    op.create_foreign_key(None, 'comments', 'article', ['article_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'avatar_hash')
    op.drop_column('comments', 'author_name')
    op.drop_column('comments', 'author_email')
    op.drop_column('comments', 'article_id')
    # ### end Alembic commands ###