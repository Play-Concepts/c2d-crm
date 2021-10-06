"""create_merchant_perk_favourites_table
Revision ID: 818c0668be17
Revises: eb2aa12852ca
Create Date: 2021-10-06 08:55:45.259931
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "818c0668be17"
down_revision = "eb2aa12852ca"
branch_labels = None
depends_on = None


def create_merchant_perk_favourites_table():
    op.create_table(
        "merchant_perk_favourites",
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
                "merchant_perks.id", name="fk_merchant_perks_merchant_perk_favourites"
            ),
            nullable=False,
        ),
        sa.Column("pda_url", sa.VARCHAR, nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("merchant_perk_id", "pda_url"),
    )


def upgrade() -> None:
    create_merchant_perk_favourites_table()


def downgrade() -> None:
    op.drop_table("merchant_perk_favourites")
