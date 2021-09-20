from app.models.core import CoreModel, IDModelMixin


class DataPassVerifierBase(CoreModel):
    name: str
    description: str
    logo_url: str


class DataPassVerifierDB(IDModelMixin, DataPassVerifierBase):
    pass


DataPassVerifierNew = DataPassVerifierBase
