import uuid

from app.db.repositories.data_passes import DataPassesRepository


async def create_data_source_and_verifier(
    data: dict, data_passes_repo: DataPassesRepository
):
    return await data_passes_repo.create_data_pass_source_(**data)


async def create_data_pass(
    data_pass_source_id: uuid.UUID,
    data: dict,
    data_passes_repo: DataPassesRepository,
):
    data_pass_data = data
    data_pass_data["data_pass_source_id"] = data_pass_source_id
    data_pass_data["data_pass_verifier_id"] = data_pass_source_id
    return await data_passes_repo.create_data_pass_(**data_pass_data)
