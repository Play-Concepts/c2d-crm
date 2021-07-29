"""create_customers_log_table
Revision ID: b42b86e63910
Revises: eaec9daee0ba
Create Date: 2021-07-28 14:10:41.155771
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic
revision = 'b42b86e63910'
down_revision = 'eaec9daee0ba'
branch_labels = None
depends_on = None


def create_customers_log_table():
    op.create_table(
        "customers_log",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("pda_url", sa.VARCHAR, nullable=False),
        sa.Column("event", sa.VARCHAR, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False),
    )


def upgrade() -> None:
    create_customers_log_table()


def downgrade() -> None:
    op.drop_table("customers_log")
