#   op.create_table(
#         "data_passes",
#         sa.Column("id", UUID(as_uuid=True), primary_key=True),
#         sa.Column("name", sa.VARCHAR(50), nullable=False),
#         sa.Column("description", sa.VARCHAR(512), nullable=True),
#         sa.Column("dataspace", sa.VARCHAR(512), nullable=False),
#         sa.Column("data_provided", sa.VARCHAR(256), nullable=False),
#         sa.Column("status", sa.VARCHAR(10), nullable=False),
#         sa.Column("created_at", sa.TIMESTAMP, nullable=False),
#         sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
#     )
from Tools.scripts.patchcheck import status
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic.class_validators import validator
from pydantic.main import BaseModel
from pydantic.types import Json

from app.models.core import CoreModel, IDModelMixin, ModelDatesMixin


class StatusType(str, Enum):
    active = 'active'
    draft = 'draft'
    inactive = 'inactive'


class DataPassBase(CoreModel):
    name: str
    description: Optional[str]
    dataspace: str
    data_provided: str
    status: Optional[StatusType]


class DataPassNew(IDModelMixin, DataPassBase, ModelDatesMixin):
    status: StatusType = 'draft'
    created_at: datetime = datetime.utcnow()


class DataPassDBModel(IDModelMixin, DataPassBase, ModelDatesMixin):
    pass
