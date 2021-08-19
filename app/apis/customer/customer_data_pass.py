import uuid
from typing import List

from app.db.repositories.data_passes import DataPassesRepository
from app.models.core import IDModelMixin
from app.models.data_pass import DataPassCustomerView


async def fn_get_customer_data_passes(
    pda_url: str, data_passes_repository: DataPassesRepository
) -> List[DataPassCustomerView]:
    return await data_passes_repository.get_customer_data_passes(pda_url=pda_url)


async def fn_customer_activate_data_pass(
    data_pass_id: uuid.UUID, pda_url: str, data_passes_repository: DataPassesRepository
) -> IDModelMixin:
    return await data_passes_repository.activate_data_pass(
        pda_url=pda_url, data_pass_id=data_pass_id
    )
