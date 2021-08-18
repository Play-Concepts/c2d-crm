"""create_data_passes_table
Revision ID: e28d8c3c0eb3
Revises: e3965c94d319
Create Date: 2021-08-18 04:40:12.775964
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "e28d8c3c0eb3"
down_revision = "e3965c94d319"
branch_labels = None
depends_on = None


def create_data_passes_table():
    op.create_table(
        "data_passes",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "name", sa.VARCHAR, nullable=False, unique=True
        ),  # eg elyria-resident
        sa.Column("title", sa.VARCHAR, nullable=False),  # Elyria Resident
        sa.Column("description_for_merchants", sa.VARCHAR, nullable=True),
        sa.Column("description_for_customers", sa.VARCHAR, nullable=True),
        sa.Column("perks_url_for_merchants", sa.VARCHAR, nullable=True),
        sa.Column("perks_url_for_customers", sa.VARCHAR, nullable=True),
        sa.Column("data_pass_source_id", UUID(as_uuid=True), nullable=False),
        sa.Column("data_pass_verifier_id", UUID(as_uuid=True), nullable=False),
        sa.Column("currency_code", sa.VARCHAR, nullable=False),
        sa.Column("price", sa.NUMERIC, nullable=False, server_default=sa.text("0.0")),
        sa.Column("status", sa.VARCHAR, nullable=False),  # enabled, disabled
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("name"),
    )


def upgrade() -> None:
    create_data_passes_table()


def downgrade() -> None:
    op.drop_table("data_passes")
