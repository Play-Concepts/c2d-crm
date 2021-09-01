"""add_expiry_to_data_passes_table
Revision ID: 60e2dc8494eb
Revises: d294163e36e8
Create Date: 2021-09-01 10:33:46.045786
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "60e2dc8494eb"
down_revision = "d294163e36e8"
branch_labels = None
depends_on = None


def add_expiry_to_data_passes() -> None:
    op.add_column("data_passes", sa.Column("details_url", sa.VARCHAR, nullable=True))
    op.add_column("data_passes", sa.Column("expiry_date", sa.TIMESTAMP, nullable=True))


def upgrade() -> None:
    add_expiry_to_data_passes()


def downgrade() -> None:
    op.drop_column("data_passes", "expiry_date")
