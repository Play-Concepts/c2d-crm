"""add_claim_timestamp_to_customers
Revision ID: 2dc82837151c
Revises: 7e7fad16535e
Create Date: 2021-07-05 10:10:43.161722
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '2dc82837151c'
down_revision = '7e7fad16535e'
branch_labels = None
depends_on = None


def add_claim_timestamp_to_customers_table() -> None:
    op.add_column(
        "customers",
        sa.Column("claimed_timestamp", sa.TIMESTAMP, nullable=True)
    )


def upgrade() -> None:
    add_claim_timestamp_to_customers_table()


def downgrade() -> None:
    pass
