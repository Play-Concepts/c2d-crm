from typing import List

from app.db.repositories.merchant_perks import MerchantPerksRepository
from app.models.data_pass import DataPassMerchantView


async def fn_get_merchant_perks(
    email: str,
    merchant_perks_repository: MerchantPerksRepository,
) -> List[DataPassMerchantView]:
    return await merchant_perks_repository.get_merchant_perks(email=email)
