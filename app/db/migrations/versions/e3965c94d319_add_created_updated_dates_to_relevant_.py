"""add_created_updated_dates_to_relevant_tables
Revision ID: e3965c94d319
Revises: b35c15a7e69c
Create Date: 2021-07-30 09:06:00.233451
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'e3965c94d319'
down_revision = 'b35c15a7e69c'
branch_labels = None
depends_on = None


def _add_created_updated_dates_for(table_name: str) -> None:
    op.add_column(
        table_name, sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()"))
    )
    op.add_column(
        table_name, sa.Column("updated_at", sa.TIMESTAMP, nullable=True)
    )


def add_created_updated_dates_to_relevant_tables() -> None:
    tables = [
        "customers",
        "merchants",
    ]

    for table in tables:
        _add_created_updated_dates_for(table)


def upgrade() -> None:
    add_created_updated_dates_to_relevant_tables()


def downgrade() -> None:
    pass
