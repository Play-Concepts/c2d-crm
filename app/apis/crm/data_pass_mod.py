from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.models.core import IDModelMixin
from app.models.data_pass_source import DataPassSourceNew


async def fn_create_data_pass_source(
    data_pass_source_new: DataPassSourceNew,
    data_pass_sources_repo: DataPassSourcesRepository,
) -> IDModelMixin:
    data_pass_source = await data_pass_sources_repo.create_data_pass_source(
        data_pass_source_new=data_pass_source_new
    )

    await data_pass_sources_repo.create_data_pass_source_table(
        data_table=data_pass_source_new.data_table
    )

    return data_pass_source
