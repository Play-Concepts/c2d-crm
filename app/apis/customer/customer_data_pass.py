from typing import List

from app.db.repositories.data_passes import DataPassesRepository
from app.models.data_pass import DataPassCustomerView


async def fn_get_customer_data_passes(
    pda_url: str, data_passes_repository: DataPassesRepository
) -> List[DataPassCustomerView]:
    return await data_passes_repository.get_customer_data_passes(pda_url=pda_url)
