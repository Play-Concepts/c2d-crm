"""add_fk_to_tables
Revision ID: d294163e36e8
Revises: df9676d15176
Create Date: 2021-08-20 11:47:15.828164
"""
from alembic import op

# revision identifiers, used by Alembic
revision = "d294163e36e8"
down_revision = "df9676d15176"
branch_labels = None
depends_on = None


def set_foreign_keys_on_tables(reverse: bool):
    for key, source, reference, source_columns, reference_columns in [
        (
            "fk_data_passes_data_pass_sources",
            "data_passes",
            "data_pass_sources",
            ["data_pass_source_id"],
            ["id"],
        ),
        (
            "fk_data_passes_data_pass_sources_v",
            "data_passes",
            "data_pass_sources",
            ["data_pass_verifier_id"],
            ["id"],
        ),
        (
            "fk_data_passes_data_pass_activations",
            "data_pass_activations",
            "data_passes",
            ["data_pass_id"],
            ["id"],
        ),
        (
            "fk_scan_transactions_users",
            "scan_transactions",
            "users",
            ["user_id"],
            ["id"],
        ),
        (
            "fk_scan_transactions_data_passes",
            "scan_transactions",
            "data_passes",
            ["data_pass_id"],
            ["id"],
        ),
    ]:
        if reverse:
            op.drop_constraint(key, source)
        else:
            op.create_foreign_key(
                key, source, reference, source_columns, reference_columns
            )


def upgrade() -> None:
    set_foreign_keys_on_tables(False)


def downgrade() -> None:
    set_foreign_keys_on_tables(True)
