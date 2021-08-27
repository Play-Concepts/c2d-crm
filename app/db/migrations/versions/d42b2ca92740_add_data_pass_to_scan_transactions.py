"""add_data_pass_to_scan_transactions
Revision ID: d42b2ca92740
Revises: ef8132dc311f
Create Date: 2021-08-19 09:40:18.347961
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "d42b2ca92740"
down_revision = "ef8132dc311f"
branch_labels = None
depends_on = None


def add_data_pass_to_scan_transactions_table() -> None:
    op.add_column(
        "scan_transactions",
        sa.Column("data_pass_id", UUID(as_uuid=True), nullable=True),
    )


def upgrade() -> None:
    add_data_pass_to_scan_transactions_table()


def downgrade() -> None:
    op.drop_column("scan_transactions", "data_pass_id")
