"""empty message

Revision ID: 129a2b5530e4
Revises: efdaba1b337f
Create Date: 2020-10-07 18:15:05.767295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '129a2b5530e4'
down_revision = 'efdaba1b337f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hd_user_base', sa.Column('public_id', sa.String(length=100), nullable=True))
    op.create_unique_constraint(None, 'hd_user_base', ['public_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'hd_user_base', type_='unique')
    op.drop_column('hd_user_base', 'public_id')
    # ### end Alembic commands ###
