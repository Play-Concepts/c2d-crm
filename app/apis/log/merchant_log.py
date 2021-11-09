import uuid

from app.db.repositories.merchant_log import MerchantLogRepository
from app.models.merchant_log import MerchantLogNew, MerchantLogNewResponse


async def fn_log_merchant_activity(
    user_id: uuid.UUID,
    component: str,
    component_identifier: uuid.UUID,
    event: str,
    merchant_log_repository: MerchantLogRepository,
) -> MerchantLogNewResponse:
    return await merchant_log_repository.log_merchant(
        merchant_log_new=MerchantLogNew(
            user_id=user_id,
            component=component,
            component_identifier=component_identifier,
            event=event,
        )
    )
