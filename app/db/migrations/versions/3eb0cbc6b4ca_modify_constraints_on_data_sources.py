"""modify_constraints_on_data_sources
Revision ID: 3eb0cbc6b4ca
Revises: cc807764cf1e
Create Date: 2021-09-16 11:39:06.003199
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '3eb0cbc6b4ca'
down_revision = 'cc807764cf1e'
branch_labels = None
depends_on = None

def modify_verifier_constraints():
    op.drop_constraint("fk_data_passes_data_pass_sources_v", "data_passes")
    op.create_foreign_key(
        "fk_data_passes_data_pass_verifiers", "data_passes", "data_pass_verifiers", ["data_pass_verifier_id"], ["id"]
    )

def upgrade() -> None:
    modify_verifier_constraints()

def downgrade() -> None:
    op.drop_constraint("fk_data_passes_data_pass_verifiers", "data_passes")
    op.create_foreign_key(
        "fk_data_passes_data_pass_sources_v", "data_passes", "data_pass_verifiers", ["data_pass_verifier_id"], ["id"]
    )
    