"""add collection_stats table

Revision ID: 65c33241eadd
Revises: e1565077c2e5
Create Date: 2022-06-10 13:21:11.760698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65c33241eadd'
down_revision = 'e1565077c2e5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'collection_stats',
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('contract_address', sa.String, nullable=False),

        sa.Column('one_day_volume', sa.Float, nullable=True),
        sa.Column('one_day_change', sa.Float, nullable=True),
        sa.Column('one_day_sales', sa.Integer, nullable=True),
        sa.Column('one_day_average_price', sa.Float, nullable=True),

        sa.Column('seven_day_volume', sa.Float, nullable=True),
        sa.Column('seven_day_change', sa.Float, nullable=True),
        sa.Column('seven_day_sales', sa.Integer, nullable=True),
        sa.Column('seven_day_average_price', sa.Float, nullable=True),

        sa.Column('thirty_day_volume', sa.Float, nullable=True),
        sa.Column('thirty_day_change', sa.Float, nullable=True),
        sa.Column('thirty_day_sales', sa.Integer, nullable=True),
        sa.Column('thirty_day_average_price', sa.Float, nullable=True),

        sa.Column('total_volume', sa.Float, nullable=True),
        sa.Column('total_sales', sa.Integer, nullable=True),
        sa.Column('total_supply', sa.Integer, nullable=True),
        sa.Column('total_minted', sa.Integer, nullable=True),
        sa.Column('num_owners', sa.Integer, nullable=True),

        sa.Column('average_price', sa.Float, nullable=True),
        sa.Column('market_cap', sa.Float, nullable=True),
        sa.Column('floor_price', sa.Float, nullable=True),

        sa.Column(
            'updated_date', sa.DateTime(timezone=True), nullable=True),

        sa.Column('_created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('_updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_index(
        'collection_stats_idx_contract_address',
        'collection_stats',
        ['contract_address'],
    )


def downgrade():
    op.drop_table('collection_stats')
