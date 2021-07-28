"""create_data_passes_table
Revision ID: 50cf7b0c5981
Revises: eaec9daee0ba
Create Date: 2021-07-28 08:40:18.515537
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSON, UUID


# revision identifiers, used by Alembic
revision = '50cf7b0c5981'
down_revision = 'eaec9daee0ba'
branch_labels = None
depends_on = None


def create_data_passes_table():
    op.create_table(
        "data_passes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.VARCHAR, nullable=False),
        sa.Column("description", sa.VARCHAR, nullable=True),
        sa.Column("dataspace", sa.VARCHAR, nullable=False),
        sa.Column("data_provided", sa.VARCHAR, nullable=False),
        sa.Column("status", sa.VARCHAR, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
    )


def upgrade() -> None:
    create_data_passes_table()


def downgrade() -> None:
    op.drop_table("data_passes")
