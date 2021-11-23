"""create_merchant_payments_table
Revision ID: 8126c5f1aae5
Revises: 803814d41740
Create Date: 2021-11-23 17:06:19.942701
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "8126c5f1aae5"
down_revision = "803814d41740"
branch_labels = None
depends_on = None


def create_merchant_payments_table():
    op.create_table(
        "merchant_payments",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", name="fk_users_merchant_payments"),
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.INTEGER,
            nullable=False,
        ),
        sa.Column(
            "payment_identifier",
            sa.VARCHAR,
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.VARCHAR,
            nullable=False,
            comment="new, manual, canceled, completed etc.",
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )


def upgrade() -> None:
    create_merchant_payments_table()


def downgrade() -> None:
    op.drop_table("merchant_payments")
