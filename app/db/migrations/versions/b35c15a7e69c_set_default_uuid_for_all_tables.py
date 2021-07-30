"""set_default_uuid_for_all_tables
Revision ID: b35c15a7e69c
Revises: 51618267f7dd
Create Date: 2021-07-29 11:30:43.384292
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'b35c15a7e69c'
down_revision = '51618267f7dd'
branch_labels = None
depends_on = None


def _set_default_uuid_for(table_name: str) -> None:
    with op.batch_alter_table(table_name) as table:
        table.alter_column("id", server_default=sa.text("uuid_generate_v4()"))


def set_default_uuid_for_all_tables() -> None:
    tables = [
        "customers",
        "merchants",
        "scan_transactions",
        "users",
    ]

    for table in tables:
        _set_default_uuid_for(table)


def set_defaults_for_customers_log_table() -> None:
    with op.batch_alter_table("customers_log") as table:
        table.alter_column("id", server_default=sa.text("uuid_generate_v4()"))
        table.alter_column("created_at", server_default=sa.text("now()"))


def upgrade() -> None:
    set_default_uuid_for_all_tables()
    set_defaults_for_customers_log_table()


def downgrade() -> None:
    pass
