"""empty message

Revision ID: 012a66ee31f7
Revises: 681eb0f8ad46
Create Date: 2016-10-02 09:44:16.875017

"""

# revision identifiers, used by Alembic.
revision = '012a66ee31f7'
down_revision = '681eb0f8ad46'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    ### end Alembic commands ###
