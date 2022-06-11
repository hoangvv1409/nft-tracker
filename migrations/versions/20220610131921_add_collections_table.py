"""add collections table

Revision ID: e1565077c2e5
Revises:
Create Date: 2022-06-10 13:19:21.106541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1565077c2e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'collections',
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('contract_address', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('symbol', sa.String, nullable=True),
        sa.Column('chain', sa.String, nullable=False),
        sa.Column('type', sa.String, nullable=False),

        sa.Column('logo', sa.String, nullable=True),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('official_site', sa.String, nullable=True),
        sa.Column('created_date', sa.DateTime(timezone=True), nullable=True),

        sa.Column('provider_payload', sa.JSON, nullable=True),

        sa.Column('_created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('_updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_unique_constraint(
        'collections_uniq', 'collections', ['contract_address', 'chain']
    )


def downgrade():
    op.drop_table('collections')
