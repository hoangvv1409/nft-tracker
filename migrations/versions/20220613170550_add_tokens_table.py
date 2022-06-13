"""add tokens table

Revision ID: 77fc2ea2022d
Revises: 65c33241eadd
Create Date: 2022-06-13 17:05:50.738427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77fc2ea2022d'
down_revision = '65c33241eadd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tokens',
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('token_id', sa.String, nullable=False),
        sa.Column('contract_address', sa.String, nullable=False),
        sa.Column('metadata', sa.JSON, nullable=True),
        sa.Column('provider_payload', sa.JSON, nullable=True),

        sa.Column('_created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('_updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_unique_constraint(
        'tokens_uniq', 'tokens', ['contract_address', 'token_id']
    )


def downgrade():
    op.drop_table('tokens')
