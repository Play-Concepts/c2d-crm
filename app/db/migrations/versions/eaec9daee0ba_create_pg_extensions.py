"""create_pg_extensions
Revision ID: eaec9daee0ba
Revises: 7aa1dcd5b9f1
Create Date: 2021-07-19 15:09:49.464153
"""
from alembic import op
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic
revision = 'eaec9daee0ba'
down_revision = '7aa1dcd5b9f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(text('CREATE EXTENSION IF NOT EXISTS "pgcrypto";'))
    op.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))


def downgrade() -> None:
    op.execute(text('DROP EXTENSION IF EXISTS "pgcrypto";'))
    op.execute(text('DROP EXTENSION IF EXISTS "uuid-ossp";'))
