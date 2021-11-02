"""remove_enums_from_activity_logs_table
Revision ID: d58926c0c666
Revises: 17d040b63843
Create Date: 2021-11-02 16:41:35.124565
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic
revision = "d58926c0c666"
down_revision = "17d040b63843"
branch_labels = None
depends_on = None


def _update_activity_logs_columns():
    op.alter_column(
        "activity_log",
        "component",
        type_=sa.VARCHAR,
    )
    op.execute("update activity_log set component='offer' where component='perk';")

    op.alter_column(
        "activity_log",
        "event",
        type_=sa.VARCHAR,
    )
    op.execute(
        "update activity_log set event='offer_link_clicked' where event='perk_link_clicked';"
    )


def _drop_enums():
    op.execute("drop type if exists activity_log_component_type;")
    op.execute("drop type if exists activity_log_event_type;")


def upgrade() -> None:
    _update_activity_logs_columns()
    _drop_enums()


def downgrade() -> None:
    pass
