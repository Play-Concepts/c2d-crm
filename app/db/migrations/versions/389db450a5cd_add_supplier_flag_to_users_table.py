"""add_supplier_flag_to_users_table
Revision ID: 389db450a5cd
Revises: 10ee92f6361f
Create Date: 2021-09-14 09:59:15.875655
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "389db450a5cd"
down_revision = "10ee92f6361f"
branch_labels = None
depends_on = None


def add_is_supplier_to_users() -> None:
    op.add_column(
        "users",
        sa.Column(
            "is_supplier", sa.BOOLEAN, nullable=False, server_default=sa.text("false")
        ),
    )


def upgrade() -> None:
    add_is_supplier_to_users()


def downgrade() -> None:
    op.drop_column("users", "is_supplier")
