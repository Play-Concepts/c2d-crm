"""create_data_pass_sources_table
Revision ID: f3a532f145c0
Revises: e28d8c3c0eb3
Create Date: 2021-08-18 06:45:42.651849
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "f3a532f145c0"
down_revision = "e28d8c3c0eb3"
branch_labels = None
depends_on = None


def create_data_pass_sources_table():
    op.create_table(
        "data_pass_sources",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "name", sa.VARCHAR, nullable=False, unique=True
        ),  # eg elyria-resident
        sa.Column("description", sa.VARCHAR, nullable=False),  # eg elyria-resident
        sa.Column("logo_url", sa.VARCHAR, nullable=False),  # Elyria Resident
        sa.Column(
            "is_data_source",
            sa.BOOLEAN,
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "is_data_verifier",
            sa.BOOLEAN,
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("name"),
    )


def upgrade() -> None:
    create_data_pass_sources_table()


def downgrade() -> None:
    op.drop_table("data_pass_sources")
