"""create_merchant_perks_data_passes_table
Revision ID: eb2aa12852ca
Revises: 0ba4a95f0213
Create Date: 2021-10-06 07:56:42.378521
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "eb2aa12852ca"
down_revision = "0ba4a95f0213"
branch_labels = None
depends_on = None


def create_merchant_perks_data_passes_table():
    op.create_table(
        "merchant_perks_data_passes",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "merchant_perk_id",
            UUID(as_uuid=True),
            sa.ForeignKey(
                "merchant_perks.id", name="fk_merchant_perks_merchant_perks_data_passes"
            ),
            nullable=False,
        ),
        sa.Column(
            "data_pass_id",
            UUID(as_uuid=True),
            sa.ForeignKey(
                "data_passes.id", name="fk_data_passes_merchant_perks_data_passes"
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("merchant_perk_id", "data_pass_id"),
    )


def upgrade() -> None:
    create_merchant_perks_data_passes_table()


def downgrade() -> None:
    op.drop_table("merchant_perks_data_passes")
