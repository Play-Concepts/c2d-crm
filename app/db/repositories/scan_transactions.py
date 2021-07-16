import uuid
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.repositories.base import BaseRepository
from app.models.scan_transaction import ScanTransactionNew, ScanTransactionBasicView, ScanTransactionView, \
    ScanTransactionCount

NEW_SCAN_TRANSACTION_SQL = """
    INSERT INTO scan_transactions(id, customer_id, user_id, created_at) 
    VALUES (:id, :customer_id, :user_id, now()) RETURNING id;
"""

GET_SCAN_TRANSACTIONS_SQL = """
    SELECT id, customer_id, user_id, created_at FROM scan_transactions 
    WHERE created_at>:from_date AND user_id=:user_id;
"""

GET_SCAN_TRANSACTIONS_COUNT_SQL = """
    SELECT COUNT(*) AS total, COALESCE(SUM(CASE WHEN customer_id is not null THEN 1 ELSE 0 END), 0) AS valid 
    FROM scan_transactions 
    WHERE created_at>:from_date AND user_id=:user_id;
"""


class ScanTransactionsRepository(BaseRepository):
    async def create_scan_transaction(self, *, scan_transaction: ScanTransactionNew) -> \
            Optional[ScanTransactionBasicView]:
        scan_transaction.id = uuid.uuid4()
        query_values = scan_transaction.dict()
        created_scan_transaction = await self.db.fetch_one(query=NEW_SCAN_TRANSACTION_SQL, values=query_values)

        return None if created_scan_transaction is None else ScanTransactionBasicView(**created_scan_transaction)

    async def get_scan_transactions_from_last_n_days(self, *, n: int, user_id: uuid.UUID) -> List[ScanTransactionView]:
        from_date = (datetime.now() - timedelta(days=n)).replace(hour=0, minute=0, second=0, microsecond=0)
        transactions = await self.db.fetch_all(query=GET_SCAN_TRANSACTIONS_SQL,
                                               values={"from_date": from_date, "user_id": user_id})

        return [ScanTransactionView(**transaction) for transaction in transactions]

    async def get_scan_transactions_count_from_last_n_days(self, *, n: int, user_id: uuid.UUID) -> ScanTransactionCount:
        from_date = (datetime.now() - timedelta(days=n)).replace(hour=0, minute=0, second=0, microsecond=0)
        transaction = await self.db.fetch_one(query=GET_SCAN_TRANSACTIONS_COUNT_SQL,
                                              values={"from_date": from_date, "user_id": user_id})

        return ScanTransactionCount(**transaction)
