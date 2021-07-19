"""create_pg_extensions
Revision ID: eaec9daee0ba
Revises: 7aa1dcd5b9f1
Create Date: 2021-07-19 15:09:49.464153
"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSON, UUID
from alembic_utils.pg_extension import  PGExtension

# revision identifiers, used by Alembic
revision = 'eaec9daee0ba'
down_revision = '7aa1dcd5b9f1'
branch_labels = None
depends_on = None

pgcrypto_extension = PGExtension(
    schema="public",
    signature="pgcrypto",
)

uuid_extension = PGExtension(
    schema="public",
    signature="uuid-ossp",
)


def upgrade() -> None:
    op.create_entity(pgcrypto_extension)
    op.create_entity(uuid_extension)


def downgrade() -> None:
    op.drop_entity(pgcrypto_extension)
    op.drop_entity(uuid_extension)
