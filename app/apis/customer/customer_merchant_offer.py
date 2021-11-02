import uuid
from typing import List, Optional, Union

from fastapi import Response, status

from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchant_offers import MerchantOffersRepository
from app.models.core import IDModelMixin
from app.models.data_pass import DataPassMerchantView, InvalidDataPass


async def fn_get_customer_offers(
    pda_url: str,
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository,
    merchant_offers_repository: MerchantOffersRepository,
    response: Response,
) -> Union[InvalidDataPass, List[DataPassMerchantView]]:
    is_valid = await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_id)
    if is_valid:
        return await merchant_offers_repository.get_customer_offers(
            pda_url=pda_url, data_pass_id=data_pass_id
        )
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()


async def fn_like_merchant_offer(
    pda_url: str,
    merchant_offer_id: uuid.UUID,
    merchant_offers_repository: MerchantOffersRepository,
) -> IDModelMixin:
    return await merchant_offers_repository.like_merchant_offer(
        pda_url=pda_url, merchant_offer_id=merchant_offer_id
    )


async def fn_unlike_merchant_offer(
    pda_url: str,
    merchant_offer_id: uuid.UUID,
    merchant_offers_repository: MerchantOffersRepository,
) -> Optional[IDModelMixin]:
    return await merchant_offers_repository.unlike_merchant_offer(
        pda_url=pda_url, merchant_offer_id=merchant_offer_id
    )


async def fn_get_customer_favourited_offers(
    pda_url: str,
    merchant_offers_repository: MerchantOffersRepository,
) -> List[DataPassMerchantView]:
    return await merchant_offers_repository.get_customer_favourited_offers(
        pda_url=pda_url
    )


async def fn_get_all_customer_offers(
    merchant_offers_repository: MerchantOffersRepository,
) -> List[DataPassMerchantView]:
    return await merchant_offers_repository.get_all_customer_offers()
