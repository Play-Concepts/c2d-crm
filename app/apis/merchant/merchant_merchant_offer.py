from typing import List

from app.db.repositories.merchant_offers import MerchantOffersRepository
from app.models.data_pass import DataPassMerchantView


async def fn_get_merchant_offers(
    email: str,
    merchant_offers_repository: MerchantOffersRepository,
) -> List[DataPassMerchantView]:
    return await merchant_offers_repository.get_merchant_offers(email=email)
