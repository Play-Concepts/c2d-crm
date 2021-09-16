from app.db.repositories.base import BaseRepository
from app.models.core import IDModelMixin
from app.models.data_pass_source import DataPassSourceNew

NEW_DATA_PASS_SOURCE_SQL = """
    INSERT INTO data_pass_sources(name, description, logo_url, data_table, search_sql, search_parameters)
    VALUES(:name, :description, :logo_url, :data_table, :search_sql, :search_parameters)
    RETURNING id
"""


class DataPassSourcesRepository(BaseRepository):
    async def create_data_pass_source(
        self, *, data_pass_source_new: DataPassSourceNew
    ) -> IDModelMixin:
        query_values = data_pass_source_new.dict()
        data_pass_source = await self.db.fetch_one(
            query=NEW_DATA_PASS_SOURCE_SQL, values=query_values
        )
        return IDModelMixin(**data_pass_source)
