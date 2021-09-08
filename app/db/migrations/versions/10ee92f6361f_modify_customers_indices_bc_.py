"""modify_customers_indices_bc_multipass
Revision ID: 10ee92f6361f
Revises: 126aaf5b95be
Create Date: 2021-09-08 10:24:50.083606
"""
from alembic import op

# revision identifiers, used by Alembic
revision = "10ee92f6361f"
down_revision = "126aaf5b95be"
branch_labels = None
depends_on = None


def modify_customers_indices_bc_multipass() -> None:
    op.drop_index("idx_customers_pda_url", "customers")
    op.create_index(
        "idx_customers_data_pass_pda_url",
        "customers",
        ["data_pass_id", "pda_url"],
        unique=True,
    )


def upgrade() -> None:
    modify_customers_indices_bc_multipass()


def downgrade() -> None:
    pass
