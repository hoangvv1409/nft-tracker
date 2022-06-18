"""add collection_transactions table

Revision ID: af5fe695beac
Revises: 77fc2ea2022d
Create Date: 2022-06-17 15:19:20.353141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af5fe695beac'
down_revision = '77fc2ea2022d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'collection_transactions',
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('transaction_hash', sa.String, unique=True),
        sa.Column('contract_address', sa.String, nullable=False),

        sa.Column('token_ids', sa.ARRAY(sa.String), nullable=False),
        sa.Column('seller_address', sa.String, nullable=False),
        sa.Column('buyer_address', sa.String, nullable=False),

        sa.Column('price', sa.DECIMAL, nullable=False),
        sa.Column('token_address', sa.String, nullable=False),
        sa.Column('currency_token', sa.String, nullable=True),

        sa.Column('provider_payload', sa.JSON, nullable=False),

        sa.Column(
            'block_timestamp', sa.DateTime(timezone=True), nullable=False),

        sa.Column('_created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('_updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_index(
        'collection_transactions_idx_token_ids',
        'collection_transactions',
        ['token_ids'],
        postgresql_using="gin",
    )

    op.create_index(
        'collection_transactionss_idx_block_timestamp',
        'collection_transactions',
        ['block_timestamp'],
        postgresql_ops={'block_timestamp': 'DESC'},
    )


def downgrade():
    op.drop_table('collection_transactions')
