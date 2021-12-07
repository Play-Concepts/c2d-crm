"""add_valid_until_to_mo_dp
Revision ID: f8341400eafe
Revises: 442551f5fb8d
Create Date: 2021-12-07 11:42:11.921528
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "f8341400eafe"
down_revision = "442551f5fb8d"
branch_labels = None
depends_on = None


def add_valid_until_to_merchant_offers_data_passes():
    op.add_column(
        "merchant_offers_data_passes",
        sa.Column("valid_until", sa.TIMESTAMP, nullable=True),
    )
    # active, inactive
    op.add_column(
        "merchant_offers_data_passes",
        sa.Column(
            "status", sa.VARCHAR, nullable=False, server_default=sa.text("'active'")
        ),
    )


def upgrade() -> None:
    add_valid_until_to_merchant_offers_data_passes()


def downgrade() -> None:
    op.drop_column("merchant_offers_data_passes", "valid_until")
    op.drop_column("merchant_offers_data_passes", "status")
