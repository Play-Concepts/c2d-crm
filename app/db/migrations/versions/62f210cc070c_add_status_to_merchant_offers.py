"""add_status_to_merchant_offers
Revision ID: 62f210cc070c
Revises: a1f21c3c7bd5
Create Date: 2021-11-14 20:01:55.022714
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "62f210cc070c"
down_revision = "a1f21c3c7bd5"
branch_labels = None
depends_on = None


def add_status_to_merchant_offers(reverse: bool = False):
    if reverse:
        op.drop_column("merchant_offers", "status")
    else:
        op.add_column(
            "merchant_offers",
            sa.Column(
                "status",
                sa.VARCHAR,
                nullable=True,
                server_default=sa.text("'new'"),
            ),
        )
        op.execute("UPDATE merchant_offers SET status='active'")
        op.alter_column("merchant_offers", "status", nullable=False)


def upgrade() -> None:
    add_status_to_merchant_offers()


def downgrade() -> None:
    add_status_to_merchant_offers(True)
