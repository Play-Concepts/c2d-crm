"""create_data_pass_verifiers_table
Revision ID: f1053b154083
Revises: 389db450a5cd
Create Date: 2021-09-16 07:29:49.067888
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "f1053b154083"
down_revision = "389db450a5cd"
branch_labels = None
depends_on = None


def create_data_pass_verifiers_table():
    op.create_table(
        "data_pass_verifiers",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("name", sa.VARCHAR, nullable=False, unique=True),
        sa.Column("description", sa.VARCHAR, nullable=False),
        sa.Column("logo_url", sa.VARCHAR, nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("name"),
    )


def upgrade() -> None:
    create_data_pass_verifiers_table()


def downgrade() -> None:
    op.drop_table("data_pass_verifiers")
