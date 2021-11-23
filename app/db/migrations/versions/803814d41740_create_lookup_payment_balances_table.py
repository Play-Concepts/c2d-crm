"""create_lookup_payment_balances_table
Revision ID: 803814d41740
Revises: 62f210cc070c
Create Date: 2021-11-23 16:49:00.888969
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "803814d41740"
down_revision = "62f210cc070c"
branch_labels = None
depends_on = None


def create_lookup_payment_balances_table():
    op.create_table(
        "lookup_payment_balances",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "currency",
            sa.VARCHAR,
            unique=True,
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.INTEGER,
            nullable=False,
        ),
        sa.Column(
            "creditable_balance",
            sa.INTEGER,
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )


def upgrade() -> None:
    create_lookup_payment_balances_table()


def downgrade() -> None:
    op.drop_table("lookup_payment_balances")
