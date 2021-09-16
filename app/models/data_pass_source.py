from app.models.core import CoreModel, IDModelMixin


class DataPassSourceBase(CoreModel):
    name: str
    description: str
    logo_url: str
    data_table: str
    search_sql: str
    search_parameters: str


class DataPassSourceDB(IDModelMixin, DataPassSourceBase):
    pass


DataPassSourceNew = DataPassSourceBase
