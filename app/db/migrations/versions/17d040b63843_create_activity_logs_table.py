"""create_activity_logs_table
Revision ID: 17d040b63843
Revises: 818c0668be17
Create Date: 2021-10-12 17:24:55.889180
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic
revision = "17d040b63843"
down_revision = "818c0668be17"
branch_labels = None
depends_on = None

activity_log_component_type = sa.Enum(
    "perk", "data_pass", name="activity_log_component_type"
)
activity_log_event_type = sa.Enum(
    "view_entered",
    "view_exited",
    "liked",
    "unliked",
    "activated",
    "deactivated",
    name="activity_log_event_type",
)


def drop_enums():
    activity_log_component_type.drop(op.get_bind(), checkfirst=True)
    activity_log_event_type.drop(op.get_bind(), checkfirst=True)


def create_activity_log_table():
    op.create_table(
        "activity_log",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("component", type_=activity_log_component_type, nullable=False),
        sa.Column("component_identifier", UUID(as_uuid=True), nullable=False),
        sa.Column("event", type_=activity_log_event_type, nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
    )


def upgrade() -> None:
    create_activity_log_table()


def downgrade() -> None:
    op.drop_table("activity_log")
    drop_enums()
