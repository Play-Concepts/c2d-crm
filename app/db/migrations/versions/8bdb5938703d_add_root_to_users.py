"""add_root_to_users
Revision ID: 8bdb5938703d
Revises: f7a36107bdcd
Create Date: 2021-07-05 12:09:37.960281
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '8bdb5938703d'
down_revision = 'f7a36107bdcd'
branch_labels = None
depends_on = None


def add_extensions() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"pgcrypto\"")


def add_root_to_users() -> None:
    op.execute("INSERT INTO users(id, email, hashed_password, is_active, "
               "is_superuser, is_verified, password_change_token) "
               "VALUES (uuid_generate_v4(), 'root@localhost', crypt('password', gen_salt('bf', 10)), true, "
               "true, true, null)")


def upgrade() -> None:
    add_extensions()
    add_root_to_users()


def downgrade() -> None:
    pass
