"""create_main_tables
Revision ID: 7e7fad16535e
Revises: 
Create Date: 2021-05-17 18:50:49.687522
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid

# revision identifiers, used by Alembic
revision = '7e7fad16535e'
down_revision = None
branch_labels = None
depends_on = None


def create_citizens_table() -> None:
    op.create_table(
        "citizens",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("data", JSON, nullable=False),
        sa.Column("status", sa.VARCHAR(10), nullable=False),
        sa.Column("pda_url", sa.VARCHAR(255), nullable=True)
    )


def upgrade() -> None:
    create_citizens_table()


def downgrade() -> None:
    op.drop_table("citizens")
