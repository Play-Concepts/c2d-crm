from app.models.merchant_log import MerchantLogNew, MerchantLogNewResponse

from .base import BaseRepository

NEW_MERCHANT_LOG_SQL = """
    INSERT INTO merchant_log(user_id, component, component_identifier, event)
    VALUES(:user_id, :component, :component_identifier, :event)
    RETURNING id, created_at;
"""


class MerchantLogRepository(BaseRepository):
    async def log_merchant(
        self, *, merchant_log_new: MerchantLogNew
    ) -> MerchantLogNewResponse:
        query_values = merchant_log_new.dict()

        created_merchant_log = await self.db.fetch_one(
            query=NEW_MERCHANT_LOG_SQL, values=query_values
        )
        return MerchantLogNewResponse(**created_merchant_log)
