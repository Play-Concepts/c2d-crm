"""add_created_at_to_scan_transactions
Revision ID: 1523f2cfd456
Revises: e3965c94d319
Create Date: 2021-08-18 19:51:52.959913
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "1523f2cfd456"
down_revision = "e3965c94d319"
branch_labels = None
depends_on = None


def add_created_at_default_to_scan_transactions() -> None:
    with op.batch_alter_table("scan_transactions") as table:
        table.alter_column("created_at", server_default=sa.text("now()"))


def upgrade() -> None:
    add_created_at_default_to_scan_transactions()


def downgrade() -> None:
    pass
