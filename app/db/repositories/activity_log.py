from app.models.activity_log import ActivityLogNew, ActivityLogNewResponse

from .base import BaseRepository

NEW_ACTIVITY_LOG_SQL = """
    INSERT INTO activity_log(component, component_identifier, event)
    VALUES(:component, :component_identifier, :event)
    RETURNING id, created_at;
"""


class ActivityLogRepository(BaseRepository):
    async def log_activity(
        self, *, activity_log_new: ActivityLogNew
    ) -> ActivityLogNewResponse:
        query_values = activity_log_new.dict()

        created_activity_log = await self.db.fetch_one(
            query=NEW_ACTIVITY_LOG_SQL, values=query_values
        )
        return ActivityLogNewResponse(**created_activity_log)