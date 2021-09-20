"""add_sqlers_data_pass_sources
Revision ID: cc807764cf1e
Revises: f1053b154083
Create Date: 2021-09-16 07:35:42.910433
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSON, UUID

# revision identifiers, used by Alembic
revision = "cc807764cf1e"
down_revision = "f1053b154083"
branch_labels = None
depends_on = None


def remove_redundant_columns(reverse: bool = False) -> None:
    if not reverse:
        op.drop_column("data_pass_sources", "is_data_source")
        op.drop_column("data_pass_sources", "is_data_verifier")
    else:
        op.add_column(
            "data_pass_sources",
            sa.Column(
                "is_data_source",
                sa.BOOLEAN,
                nullable=False,
                server_default=sa.text("true"),
            ),
        )
        op.add_column(
            "data_pass_sources",
            sa.Column(
                "is_data_verifier",
                sa.BOOLEAN,
                nullable=False,
                server_default=sa.text("true"),
            ),
        )


def add_sqlers_to_data_pass_sources(reverse: bool = False) -> None:
    if not reverse:
        op.add_column(
            "data_pass_sources",
            sa.Column(
                "data_table", sa.VARCHAR, nullable=False, server_default=sa.text("''")
            ),
        )
        op.add_column(
            "data_pass_sources",
            sa.Column(
                "search_sql", sa.VARCHAR, nullable=False, server_default=sa.text("''")
            ),
        )
        op.add_column(
            "data_pass_sources",
            sa.Column(
                "data_descriptors",
                JSON,
                nullable=False,
                server_default=sa.text("'{}'"),
            ),
        )
        op.add_column(
            "data_pass_sources",
            sa.Column(
                "user_id",
                UUID(as_uuid=True),
                nullable=True,
            ),
        )
    else:
        op.drop_column("data_pass_sources", "data_table")
        op.drop_column("data_pass_sources", "search_sql")
        op.drop_column("data_pass_sources", "data_descriptors")
        op.drop_column("data_pass_sources", "user_id")


def upgrade() -> None:
    remove_redundant_columns()
    add_sqlers_to_data_pass_sources()


def downgrade() -> None:
    remove_redundant_columns(True)
    add_sqlers_to_data_pass_sources(True)
