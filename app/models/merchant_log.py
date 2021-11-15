import uuid

from app.models.core import CoreModel, CreatedAtMixin, IDModelMixin


class MerchantLogBase(CoreModel):
    user_id: uuid.UUID
    component: str
    component_identifier: uuid.UUID
    event: str


MerchantLogNew = MerchantLogBase


class MerchantLogDBModel(IDModelMixin, MerchantLogBase, CreatedAtMixin):
    pass


MerchantLog = MerchantLogDBModel
