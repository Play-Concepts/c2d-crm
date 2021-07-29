"""add_agreement_check_to_merchants_table
Revision ID: 51618267f7dd
Revises: b42b86e63910
Create Date: 2021-07-29 07:16:39.062553
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '51618267f7dd'
down_revision = 'b42b86e63910'
branch_labels = None
depends_on = None


def add_agreement_check_to_merchants_table() -> None:
    op.add_column(
        "merchants",
        sa.Column("terms_agreed", sa.BOOLEAN, nullable=False, server_default="false"),
    )


def upgrade() -> None:
    add_agreement_check_to_merchants_table()


def downgrade() -> None:
    op.drop_column("merchants", "terms_agreed")
