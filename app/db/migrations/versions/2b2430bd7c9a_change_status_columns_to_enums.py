"""change_status_columns_to_enums
Revision ID: 2b2430bd7c9a
Revises: d42b2ca92740
Create Date: 2021-08-19 12:28:51.846586
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "2b2430bd7c9a"
down_revision = "d42b2ca92740"
branch_labels = None
depends_on = None


claim_status_type = sa.Enum("new", "claimed", name="claim_status_type")
active_status_type = sa.Enum("active", "inactive", name="active_status_type")


def create_enums():
    claim_status_type.create(op.get_bind(), checkfirst=True)
    active_status_type.create(op.get_bind(), checkfirst=True)


def drop_enums():
    claim_status_type.drop(op.get_bind())
    active_status_type.drop(op.get_bind())


def change_status_columns_to_enums():
    _update_customers_status_column()
    _update_data_pass_tables_status_columns()


def _update_customers_status_column():
    op.alter_column(
        "customers",
        "status",
        existing_type=sa.VARCHAR,
        type_=claim_status_type,
        server_default=sa.text("'new'"),
        postgresql_using="status::claim_status_type",
    )


def _update_data_pass_tables_status_columns():
    op.alter_column(
        "data_passes",
        "status",
        existing_type=sa.VARCHAR,
        type_=active_status_type,
        server_default=sa.text("'inactive'"),
        postgresql_using="status::active_status_type",
    )

    op.execute("alter table data_pass_activations alter column status drop default;")
    op.alter_column(
        "data_pass_activations",
        "status",
        existing_type=sa.VARCHAR,
        type_=active_status_type,
        server_default=sa.text("'active'"),
        postgresql_using="status::active_status_type",
    )


def upgrade() -> None:
    create_enums()
    change_status_columns_to_enums()


def downgrade() -> None:
    pass
