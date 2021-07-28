"""create_scan_transactions_table
Revision ID: 7aa1dcd5b9f1
Revises: 72c7db976a94
Create Date: 2021-07-16 08:42:32.772866
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic
revision = '7aa1dcd5b9f1'
down_revision = '72c7db976a94'
branch_labels = None
depends_on = None


def create_scan_transactions_table() -> None:
    op.create_table(
        "scan_transactions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False),
    )


def upgrade() -> None:
    create_scan_transactions_table()


def downgrade() -> None:
    op.drop_table("scan_transactions")
