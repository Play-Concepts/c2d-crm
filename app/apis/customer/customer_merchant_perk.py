import uuid
from typing import List, Optional, Union

from fastapi import Response, status

from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchant_perks import MerchantPerksRepository
from app.models.core import IDModelMixin
from app.models.data_pass import DataPassMerchantView, InvalidDataPass


async def fn_get_customer_perks(
    pda_url: str,
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository,
    merchant_perks_repository: MerchantPerksRepository,
    response: Response,
) -> Union[InvalidDataPass, List[DataPassMerchantView]]:
    is_valid = await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_id)
    if is_valid:
        return await merchant_perks_repository.get_customer_perks(
            pda_url=pda_url, data_pass_id=data_pass_id
        )
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()


async def fn_like_merchant_perk(
    pda_url: str,
    merchant_perk_id: uuid.UUID,
    merchant_perks_repository: MerchantPerksRepository,
) -> IDModelMixin:
    return await merchant_perks_repository.like_merchant_perk(
        pda_url=pda_url, merchant_perk_id=merchant_perk_id
    )


async def fn_unlike_merchant_perk(
    pda_url: str,
    merchant_perk_id: uuid.UUID,
    merchant_perks_repository: MerchantPerksRepository,
) -> Optional[IDModelMixin]:
    return await merchant_perks_repository.unlike_merchant_perk(
        pda_url=pda_url, merchant_perk_id=merchant_perk_id
    )


async def fn_get_customer_favourited_perks(
    pda_url: str,
    merchant_perks_repository: MerchantPerksRepository,
) -> List[DataPassMerchantView]:
    return await merchant_perks_repository.get_customer_favourited_perks(
        pda_url=pda_url
    )
