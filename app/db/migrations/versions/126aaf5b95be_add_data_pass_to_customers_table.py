"""add_data_pass_to_customers_table
Revision ID: 126aaf5b95be
Revises: 25bb83357663
Create Date: 2021-09-06 12:06:50.783835
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "126aaf5b95be"
down_revision = "25bb83357663"
branch_labels = None
depends_on = None


def add_data_pass_to_customers() -> None:
    op.add_column(
        "customers",
        sa.Column("data_pass_id", UUID(as_uuid=True), nullable=True),
    )


def update_current_data() -> None:
    sql = """
        UPDATE customers SET data_pass_id = (SELECT id FROM data_passes WHERE name = 'elyria-resident');
    """
    op.execute(sql)


def constraint_data_pass_column() -> None:
    with op.batch_alter_table("customers") as table:
        table.alter_column("data_pass_id", nullable=False)

    op.create_foreign_key(
        "fk_customers_data_passes",
        "customers",
        "data_passes",
        ["data_pass_id"],
        ["id"],
    )


def upgrade() -> None:
    add_data_pass_to_customers()
    update_current_data()
    constraint_data_pass_column()


def downgrade() -> None:
    op.drop_constraint("fk_customers_data_passes", "customers")
    op.drop_column("customers", "data_pass_id")
