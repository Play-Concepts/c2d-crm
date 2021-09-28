import uuid

from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_pass_verifiers import DataPassVerifiersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.models.data_pass_source import DataPassSourceNew
from app.models.data_pass_verifier import DataPassVerifierNew


async def create_data_source(
    data: dict, data_pass_sources_repo: DataPassSourcesRepository
):
    return await data_pass_sources_repo.create_data_pass_source(
        data_pass_source_new=DataPassSourceNew(**data)
    )


async def create_data_source_data_table(
    data_table: str, data_pass_sources_repo: DataPassSourcesRepository
):
    return await data_pass_sources_repo.create_data_pass_source_table(
        data_table=data_table
    )


async def create_data_verifier(
    data: dict, data_pass_verifiers_repo: DataPassVerifiersRepository
):
    return await data_pass_verifiers_repo.create_data_pass_verifier(
        data_pass_verifier_new=DataPassVerifierNew(**data)
    )


async def create_data_pass(
    data_pass_source_id: uuid.UUID,
    data_pass_verifier_id: uuid.UUID,
    data: dict,
    data_passes_repo: DataPassesRepository,
):
    data_pass_data = data
    data_pass_data["data_pass_source_id"] = data_pass_source_id
    data_pass_data["data_pass_verifier_id"] = data_pass_verifier_id
    return await data_passes_repo.create_data_pass_(**data_pass_data)
