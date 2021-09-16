from app.db.repositories.base import BaseRepository
from app.models.core import IDModelMixin
from app.models.data_pass_verifier import DataPassVerifierNew

NEW_DATA_PASS_SOURCE_SQL = """
    INSERT INTO data_pass_verifiers(name, description, logo_url)
    VALUES(:name, :description, :logo_url)
    RETURNING id
"""


class DataPassVerifiersRepository(BaseRepository):
    async def create_data_pass_verifier(
        self, *, data_pass_verifier_new: DataPassVerifierNew
    ) -> IDModelMixin:
        query_values = data_pass_verifier_new.dict()
        data_pass_verifier = await self.db.fetch_one(
            query=NEW_DATA_PASS_SOURCE_SQL, values=query_values
        )
        return IDModelMixin(**data_pass_verifier)
