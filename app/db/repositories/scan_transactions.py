import uuid
from typing import List, Optional, Any
from datetime import datetime, timedelta

from app.db.repositories.base import BaseRepository
from app.models.scan_transaction import ScanTransactionNew, ScanTransactionBasicView, ScanTransactionView, \
    ScanTransactionCount, ScanTransactionCounts

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
    WHERE created_at BETWEEN :from_date AND :to_date AND user_id=:user_id;
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

    async def get_scan_transactions_count_with_interval_n_days(self, *, interval_days: int, user_id: uuid.UUID) -> ScanTransactionCounts:
        first_from_date = (datetime.now() - timedelta(days=interval_days)).replace(hour=0, minute=0, second=0, microsecond=0)
        second_from_date = first_from_date - timedelta(days=interval_days)
        third_from_date = second_from_date - timedelta(days=interval_days)

        first_transaction = await self.db.fetch_one(query=GET_SCAN_TRANSACTIONS_COUNT_SQL,
                                                    values={
                                                        "from_date": first_from_date,
                                                        "to_date": datetime.now(),
                                                        "user_id": user_id})

        second_transaction = await self.db.fetch_one(query=GET_SCAN_TRANSACTIONS_COUNT_SQL,
                                                     values={
                                                        "from_date": second_from_date,
                                                        "to_date": first_from_date,
                                                        "user_id": user_id})

        third_transaction = await self.db.fetch_one(query=GET_SCAN_TRANSACTIONS_COUNT_SQL,
                                                    values={
                                                         "from_date": third_from_date,
                                                         "to_date": second_from_date,
                                                         "user_id": user_id})
        return ScanTransactionCounts(
            interval_1=ScanTransactionCount(**first_transaction).compute(),
            interval_2=ScanTransactionCount(**second_transaction).compute(),
            interval_3=ScanTransactionCount(**third_transaction).compute(),
        )

