"""empty message

Revision ID: f42fdf8496f4
Revises: 5137b683ddfb
Create Date: 2020-07-27 13:36:12.774398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f42fdf8496f4'
down_revision = '5137b683ddfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('playlist', sa.Column('isPublic', sa.Boolean(), nullable=True))
    op.add_column('playlist', sa.Column('noSongs', sa.Integer(), nullable=True))
    op.add_column('playlist', sa.Column('userId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'playlist', 'user', ['userId'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'playlist', type_='foreignkey')
    op.drop_column('playlist', 'userId')
    op.drop_column('playlist', 'noSongs')
    op.drop_column('playlist', 'isPublic')
    # ### end Alembic commands ###
