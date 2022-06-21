"""add transfer info to tokens table

Revision ID: 195d258f9eca
Revises: af5fe695beac
Create Date: 2022-06-21 21:21:41.755306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '195d258f9eca'
down_revision = 'af5fe695beac'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'tokens', sa.Column('current_price', sa.DECIMAL, nullable=True)
    )
    op.add_column(
        'tokens', sa.Column('last_price', sa.DECIMAL, nullable=True)
    )
    op.add_column(
        'tokens', sa.Column('owner_address', sa.String, nullable=True)
    )
    op.add_column(
        'tokens', sa.Column('transfer_token', sa.String, nullable=True)
    )
    op.add_column(
        'tokens', sa.Column('block_timestamp', sa.DateTime(
            timezone=True), nullable=True)
    )


def downgrade():
    op.drop_column('tokens', 'current_price')
    op.drop_column('tokens', 'last_price')
    op.drop_column('tokens', 'owner_address')
    op.drop_column('tokens', 'transfer_token')
    op.drop_column('tokens', 'block_timestamp')
