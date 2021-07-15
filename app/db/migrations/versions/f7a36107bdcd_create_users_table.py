"""create_user_tables
Revision ID: f7a36107bdcd
Revises: 7e7fad16535e
Create Date: 2021-07-02 12:34:55.254359
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic
revision = 'f7a36107bdcd'
down_revision = '2dc82837151c'
branch_labels = None
depends_on = None


# https://frankie567.github.io/fastapi-users/configuration/model.html
def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.VARCHAR(255), nullable=False),
        sa.Column("hashed_password", sa.VARCHAR(4096), nullable=False),
        sa.Column("is_active", sa.BOOLEAN, nullable=False),
        sa.Column("is_superuser", sa.BOOLEAN, nullable=False),
        sa.Column("is_verified", sa.BOOLEAN, nullable=False),
    )


def upgrade() -> None:
    create_users_table()


def downgrade() -> None:
    op.drop_table("users")
