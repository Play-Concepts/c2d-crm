"""create_data_pass_activations_table
Revision ID: ef8132dc311f
Revises: f3a532f145c0
Create Date: 2021-08-18 06:53:43.728418
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "ef8132dc311f"
down_revision = "f3a532f145c0"
branch_labels = None
depends_on = None


def create_data_pass_activations_table():
    op.create_table(
        "data_pass_activations",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("data_pass_id", UUID(as_uuid=True), nullable=False),
        sa.Column("pda_url", sa.VARCHAR, nullable=False),  # Elyria Resident
        sa.Column(
            "status", sa.VARCHAR, nullable=False, server_default=sa.text("'active'")
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("data_pass_id", "pda_url"),
    )


def upgrade() -> None:
    create_data_pass_activations_table()


def downgrade() -> None:
    op.drop_table("data_pass_activations")
