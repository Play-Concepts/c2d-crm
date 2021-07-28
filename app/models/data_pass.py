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
    title: str
    description_for_merchants: Optional[str]
    description_for_customers: Optional[str]
    dataspace: str
    data_provided: str
    status: Optional[StatusType]


class DataPassNew(IDModelMixin, DataPassBase, ModelDatesMixin):
    status: StatusType = 'draft'
    created_at: datetime = datetime.utcnow()


class DataPassUpdate(CoreModel, ModelDatesMixin):
    description_for_merchants: str
    description_for_customers: str
    updated_at: datetime = datetime.utcnow()


class DataPassDBModel(IDModelMixin, DataPassBase, ModelDatesMixin):
    pass


DataPassView = DataPassDBModel
