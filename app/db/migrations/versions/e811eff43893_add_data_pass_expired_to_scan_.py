"""add_data_pass_expired_to_scan_transactions
Revision ID: e811eff43893
Revises: 1c060c5bf679
Create Date: 2021-09-21 15:44:50.456348
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "e811eff43893"
down_revision = "1c060c5bf679"
branch_labels = None
depends_on = None


def add_data_pass_expired_to_scan_transactions(reverse: bool = False):
    if reverse:
        op.drop_column("scan_transactions", "data_pass_expired")
    else:
        op.add_column(
            "scan_transactions",
            sa.Column(
                "data_pass_expired",
                sa.BOOLEAN,
                nullable=False,
                server_default=sa.text("false"),
            ),
        )


def upgrade() -> None:
    add_data_pass_expired_to_scan_transactions()


def downgrade() -> None:
    add_data_pass_expired_to_scan_transactions(True)
