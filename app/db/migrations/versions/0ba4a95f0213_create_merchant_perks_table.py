"""create_merchant_perks_table
Revision ID: 0ba4a95f0213
Revises: e811eff43893
Create Date: 2021-10-06 06:52:43.928691
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "0ba4a95f0213"
down_revision = "e811eff43893"
branch_labels = None
depends_on = None


def create_merchant_perks_table():
    op.create_table(
        "merchant_perks",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "merchant_id",
            UUID(as_uuid=True),
            sa.ForeignKey("merchants.id", name="fk_merchants_merchant_perks"),
            nullable=False,
        ),
        sa.Column("title", sa.VARCHAR, nullable=False),  # Elyria Resident
        sa.Column("details", sa.VARCHAR, nullable=True),
        sa.Column(
            "start_date", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("end_date", sa.TIMESTAMP, nullable=True),
        sa.Column("perk_url", sa.VARCHAR, nullable=False),
        sa.Column("logo_url", sa.VARCHAR, nullable=True),
        sa.Column("perk_image_url", sa.VARCHAR, nullable=True),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )


def upgrade() -> None:
    create_merchant_perks_table()


def downgrade() -> None:
    op.drop_table("merchant_perks")
