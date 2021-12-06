"""create_merchant_balances_table
Revision ID: 442551f5fb8d
Revises: 8126c5f1aae5
Create Date: 2021-11-23 17:25:15.732497
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "442551f5fb8d"
down_revision = "8126c5f1aae5"
branch_labels = None
depends_on = None


def create_merchant_balances_table():
    op.create_table(
        "merchant_balances",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "merchant_id",
            UUID(as_uuid=True),
            sa.ForeignKey("merchants.id", name="fk_merchants_merchant_balances"),
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.INTEGER,
            nullable=False,
        ),
        sa.Column(
            "balance_type",
            sa.VARCHAR,
            nullable=False,
            comment="credit vs debit",
        ),
        sa.Column(
            "transaction_identifier",
            UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )


def upgrade() -> None:
    create_merchant_balances_table()


def downgrade() -> None:
    op.drop_table("merchant_balances")
