"""modify_expiry_info_on_data_passes
Revision ID: 1c060c5bf679
Revises: 3eb0cbc6b4ca
Create Date: 2021-09-21 13:28:37.719012
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "1c060c5bf679"
down_revision = "3eb0cbc6b4ca"
branch_labels = None
depends_on = None


def modify_expiry_info_on_data_passes(reverse: bool = False):
    if reverse:
        op.drop_column("data_passes", "expiry_days")
        op.add_column(
            "data_passes", sa.Column("expiry_date", sa.TIMESTAMP, nullable=True)
        )
    else:
        op.drop_column("data_passes", "expiry_date")
        op.add_column(
            "data_passes",
            sa.Column(
                "expiry_days", sa.INTEGER, nullable=False, server_default=sa.text("365")
            ),
        )


def upgrade() -> None:
    modify_expiry_info_on_data_passes()


def downgrade() -> None:
    modify_expiry_info_on_data_passes(True)
