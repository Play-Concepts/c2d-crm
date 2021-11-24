import uuid
from typing import List, Union

from fastapi import Response, status

from app.db.repositories.activity_log import ActivityLogRepository
from app.db.repositories.merchant_offers import MerchantOffersRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.activity_log import ActivityLogSearch
from app.models.core import DaySeriesUnit, NotFound
from app.models.merchant_offer import ForbiddenMerchantOfferAccess


async def fn_merchant_get_log_activity_daily_stats(
    merchant_email: str,
    days: int,
    component: str,
    component_identifier: uuid.UUID,
    event: str,
    activity_log_repository: ActivityLogRepository,
    merchant_repository: MerchantsRepository,
    merchant_offers_repository: MerchantOffersRepository,
    response: Response,
) -> Union[NotFound, ForbiddenMerchantOfferAccess, List[DaySeriesUnit]]:
    merchant = await merchant_repository.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")

    if component == "offer":
        is_edit_permitted = (
            await merchant_offers_repository.is_merchant_offer_updateable(
                id=component_identifier, merchant_id=merchant.id
            )
        )
        if not is_edit_permitted.value:
            response.status_code = status.HTTP_403_FORBIDDEN
            return ForbiddenMerchantOfferAccess()

    return await activity_log_repository.get_log_activity_daily_stats(
        days=days,
        activity_log_search=ActivityLogSearch(
            component=component,
            component_identifier=component_identifier,
            event=event,
        ),
    )
