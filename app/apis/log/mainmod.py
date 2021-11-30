import uuid

from app.db.repositories.activity_log import ActivityLogRepository
from app.models.activity_log import (ActivityLogComponentType,
                                     ActivityLogEventType, ActivityLogNew)
from app.models.core import NewRecordResponse

from . import log_statistics, merchant_log


async def fn_log_activity(
    component: str,
    component_identifier: uuid.UUID,
    event: str,
    activity_log_repository: ActivityLogRepository,
) -> NewRecordResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=component,
            component_identifier=component_identifier,
            event=event,
        )
    )


async def fn_log_offer_liked(
    merchant_offer_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> NewRecordResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.offer,
            component_identifier=merchant_offer_id,
            event=ActivityLogEventType.liked,
        )
    )


async def fn_log_offer_unliked(
    merchant_offer_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> NewRecordResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.offer,
            component_identifier=merchant_offer_id,
            event=ActivityLogEventType.unliked,
        )
    )


async def fn_log_data_pass_activated(
    data_pass_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> NewRecordResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.data_pass,
            component_identifier=data_pass_id,
            event=ActivityLogEventType.activated,
        )
    )


async def fn_log_data_pass_deactivated(
    data_pass_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> NewRecordResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.data_pass,
            component_identifier=data_pass_id,
            event=ActivityLogEventType.deactivated,
        )
    )


fn_log_merchant_activity = merchant_log.fn_log_merchant_activity
fn_merchant_get_log_activity_daily_stats = (
    log_statistics.fn_merchant_get_log_activity_daily_stats
)
