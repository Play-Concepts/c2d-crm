from typing import List

from .base import BaseRepository
from ...models.data_pass import DataPassView


GET_DATA_PASSES_SQL = """
    SELECT * FROM data_passes WHERE status=:status;
"""


class DataPassesRepository(BaseRepository):
    async def get_data_passes(self, *, status: str) -> List[DataPassView]:
        query_values = {
            "status": status
        }
        data_passes = await self.db.fetch_all(query=GET_DATA_PASSES_SQL, values=query_values)
        return [DataPassView(**data_pass) for data_pass in data_passes]
