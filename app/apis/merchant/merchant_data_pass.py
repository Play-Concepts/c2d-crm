from typing import List

from app.db.repositories.data_passes import DataPassesRepository
from app.models.data_pass import DataPassMerchantView


async def fn_get_merchant_data_passes(
    data_passes_repository: DataPassesRepository,
) -> List[DataPassMerchantView]:
    return await data_passes_repository.get_merchant_data_passes()
