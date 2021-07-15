"""create_merchant_table
Revision ID: 72c7db976a94
Revises: f7a36107bdcd
Create Date: 2021-07-08 15:00:35.442093
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid

# revision identifiers, used by Alembic
revision = '72c7db976a94'
down_revision = 'f7a36107bdcd'
branch_labels = None
depends_on = None


def create_merchants_table() -> None:
    op.create_table(
        "merchants",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("first_name", sa.VARCHAR(128), nullable=False),
        sa.Column("last_name", sa.VARCHAR(128), nullable=False),
        sa.Column("company_name", sa.VARCHAR(128), nullable=False),
        sa.Column("trade_name", sa.VARCHAR(128), nullable=True),
        sa.Column("address", sa.VARCHAR(4096), nullable=True),
        sa.Column("email", sa.VARCHAR(255), nullable=False, unique=True),
        sa.Column("phone_number", sa.VARCHAR(47), nullable=True),
        sa.Column("offer", JSON, nullable=True),
        sa.Column("logo_url", sa.VARCHAR(4096), nullable=True),
        sa.Column("welcome_email_sent", sa.TIMESTAMP, nullable=True),
        sa.Column("password_change_token", sa.VARCHAR(4096), nullable=True),
    )
    
    
def upgrade() -> None:
    create_merchants_table()


def downgrade() -> None:
    op.drop_table("merchants")
