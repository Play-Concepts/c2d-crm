import uuid

from app.db.repositories.activity_log import ActivityLogRepository
from app.models.activity_log import (ActivityLogComponentType,
                                     ActivityLogEventType, ActivityLogNew,
                                     ActivityLogNewResponse)


async def fn_log_perk_view_entered(
    merchant_perk_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.perk,
            component_identifier=merchant_perk_id,
            event=ActivityLogEventType.view_entered,
        )
    )


async def fn_log_perk_view_exited(
    merchant_perk_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.perk,
            component_identifier=merchant_perk_id,
            event=ActivityLogEventType.view_exited,
        )
    )


async def fn_log_perk_liked(
    merchant_perk_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.perk,
            component_identifier=merchant_perk_id,
            event=ActivityLogEventType.liked,
        )
    )


async def fn_log_perk_unliked(
    merchant_perk_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.perk,
            component_identifier=merchant_perk_id,
            event=ActivityLogEventType.unliked,
        )
    )


async def fn_log_data_pass_view_entered(
    data_pass_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.data_pass,
            component_identifier=data_pass_id,
            event=ActivityLogEventType.view_entered,
        )
    )


async def fn_log_data_pass_view_exited(
    data_pass_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.data_pass,
            component_identifier=data_pass_id,
            event=ActivityLogEventType.view_exited,
        )
    )


async def fn_log_data_pass_info_view_entered(
    data_pass_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.data_pass,
            component_identifier=data_pass_id,
            event=ActivityLogEventType.info_view_entered,
        )
    )


async def fn_log_data_pass_info_view_exited(
    data_pass_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.data_pass,
            component_identifier=data_pass_id,
            event=ActivityLogEventType.info_view_exited,
        )
    )


async def fn_log_data_pass_activated(
    data_pass_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
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
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.data_pass,
            component_identifier=data_pass_id,
            event=ActivityLogEventType.deactivated,
        )
    )


async def fn_log_data_pass_perk_link_clicked(
    data_pass_id: uuid.UUID,
    activity_log_repository: ActivityLogRepository,
) -> ActivityLogNewResponse:
    return await activity_log_repository.log_activity(
        activity_log_new=ActivityLogNew(
            component=ActivityLogComponentType.data_pass,
            component_identifier=data_pass_id,
            event=ActivityLogEventType.perk_link_clicked,
        )
    )
