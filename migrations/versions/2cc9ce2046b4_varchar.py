"""varchar

Revision ID: 2cc9ce2046b4
Revises: fbc3e6e571b6
Create Date: 2022-06-02 10:07:56.151008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cc9ce2046b4'
down_revision = 'fbc3e6e571b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('venues_facebook_link_key', 'venues', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('venues_facebook_link_key', 'venues', ['facebook_link'])
    # ### end Alembic commands ###