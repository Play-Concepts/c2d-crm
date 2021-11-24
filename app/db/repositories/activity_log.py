from typing import List

from app.models.activity_log import ActivityLogNew, ActivityLogSearch
from app.models.core import DaySeriesUnit, NewRecordResponse

from .base import BaseRepository

NEW_ACTIVITY_LOG_SQL = """
    INSERT INTO activity_log(component, component_identifier, event)
    VALUES(:component, :component_identifier, :event)
    RETURNING id, created_at;
"""

ACTIVITY_LOG_DAILY_STATS_SQL = """
    SELECT day, COALESCE(imp_count, 0) AS count
    FROM  (
    SELECT day::date
    FROM generate_series(current_date - interval '{days}' day, current_date, interval  '1 day') day
    ) d
    LEFT JOIN (
        SELECT date_trunc('day', created_at) AS day,
        count(*) AS imp_count
        FROM activity_log
            WHERE component = :component
            AND event = :event
            AND component_identifier = :component_identifier
            GROUP BY 1
    ) t USING (day)
    ORDER BY day;
"""


class ActivityLogRepository(BaseRepository):
    async def log_activity(
        self, *, activity_log_new: ActivityLogNew
    ) -> NewRecordResponse:
        query_values = activity_log_new.dict()

        created_activity_log = await self.db.fetch_one(
            query=NEW_ACTIVITY_LOG_SQL, values=query_values
        )
        return NewRecordResponse(**created_activity_log)

    async def get_log_activity_daily_stats(
        self, *, activity_log_search: ActivityLogSearch, days: int
    ) -> List[DaySeriesUnit]:
        query_values = activity_log_search.dict()

        activity_logs = await self.db.fetch_all(
            query=ACTIVITY_LOG_DAILY_STATS_SQL.format(days=days), values=query_values
        )
        return [DaySeriesUnit(**activity_log) for activity_log in activity_logs]
