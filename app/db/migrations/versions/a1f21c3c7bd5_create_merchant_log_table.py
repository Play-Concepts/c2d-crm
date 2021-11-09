"""create_merchant_log_table
Revision ID: a1f21c3c7bd5
Revises: d54b59a3ba3b
Create Date: 2021-11-09 18:02:15.926999
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "a1f21c3c7bd5"
down_revision = "d54b59a3ba3b"
branch_labels = None
depends_on = None


def create_merchant_log_table():
    op.create_table(
        "merchant_log",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", name="fk_users_merchant_log"),
            nullable=False,
        ),
        sa.Column("component", sa.VARCHAR, nullable=False),
        sa.Column("component_identifier", UUID(as_uuid=True), nullable=False),
        sa.Column("event", sa.VARCHAR, nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
    )


def upgrade() -> None:
    create_merchant_log_table()


def downgrade() -> None:
    op.drop_table("merchant_log")
