"""add_indices_to_tables
Revision ID: df9676d15176
Revises: 2b2430bd7c9a
Create Date: 2021-08-20 09:45:15.010831
"""
from alembic import op

# revision identifiers, used by Alembic
revision = "df9676d15176"
down_revision = "2b2430bd7c9a"
branch_labels = None
depends_on = None


def set_indices_on_tables(reverse: bool):
    for index, table, columns, is_unique in [
        ("idx_users_email", "users", ["email"], True),
        ("idx_merchants_email", "merchants", ["email"], True),
        ("idx_customers_pda_url", "customers", ["pda_url"], True),
        ("idx_scan_transactions_user_id", "scan_transactions", ["user_id"], False),
        (
            "idx_scan_transactions_customer_id",
            "scan_transactions",
            ["customer_id"],
            False,
        ),
        (
            "idx_scan_transactions_data_pass_id",
            "scan_transactions",
            ["data_pass_id"],
            False,
        ),
    ]:
        if reverse:
            op.drop_index(index)
        else:
            op.create_index(index, table, columns, unique=is_unique)


def upgrade() -> None:
    set_indices_on_tables(False)


def downgrade() -> None:
    set_indices_on_tables(True)
