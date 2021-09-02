"""add_validity_to_scan_transactions_table
Revision ID: 25bb83357663
Revises: 60e2dc8494eb
Create Date: 2021-09-02 15:34:58.603985
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '25bb83357663'
down_revision = '60e2dc8494eb'
branch_labels = None
depends_on = None


def add_validity_to_scan_transactions() -> None:
    op.add_column("scan_transactions", sa.Column("data_pass_verified_valid", sa.BOOLEAN, nullable=True))


def upgrade() -> None:
    add_validity_to_scan_transactions()


def downgrade() -> None:
    op.drop_column("scan_transactions", "data_pass_verified_valid")
