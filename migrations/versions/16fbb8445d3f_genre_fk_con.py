"""genre_fk_con

Revision ID: 16fbb8445d3f
Revises: 9df90229032d
Create Date: 2022-06-01 15:56:01.585778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16fbb8445d3f'
down_revision = '9df90229032d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genres', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('genres', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genres', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('genres', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###