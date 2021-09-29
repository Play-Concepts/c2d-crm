import uuid
from datetime import datetime, timedelta
from typing import Optional, Union

from app.db.repositories.base import BaseRepository
from app.models.scan_transaction import (ScanTransactionBasicView,
                                         ScanTransactionCount,
                                         ScanTransactionCounts,
                                         ScanTransactionNew,
                                         ScanTransactionNewTest)

NEW_SCAN_TRANSACTION_SQL = """
    INSERT INTO scan_transactions(customer_id, user_id, data_pass_id, data_pass_verified_valid, data_pass_expired)
    VALUES (:customer_id, :user_id, :data_pass_id, :data_pass_verified_valid, :data_pass_expired) RETURNING id;
"""

NEW_SCAN_TRANSACTION_TEST_SQL_ = """
    INSERT INTO scan_transactions(customer_id, user_id, data_pass_id, data_pass_verified_valid,
    data_pass_expired, created_at)
    VALUES (:customer_id, :user_id, :data_pass_id, :data_pass_verified_valid, :data_pass_expired,
    :created_at) RETURNING id;
"""

GET_SCAN_TRANSACTIONS_COUNT_SQL = """
    SELECT COUNT(*) AS total, COALESCE(SUM(CASE WHEN customer_id is not null THEN 1 ELSE 0 END), 0) AS valid,
    CAST(:from_date AS timestamp) as from_date, CAST(:to_date AS timestamp) as to_date
    FROM scan_transactions
    WHERE created_at BETWEEN :from_date AND :to_date AND user_id=:user_id AND data_pass_id=:data_pass_id;
"""

GET_CUSTOMER_SCAN_TRANSACTIONS_COUNT_SQL = """
    SELECT COUNT(*) AS total, COALESCE(SUM(CASE WHEN user_id is not null THEN 1 ELSE 0 END), 0) AS valid,
    CAST(:from_date AS timestamp) as from_date, CAST(:to_date AS timestamp) as to_date
    FROM scan_transactions
    WHERE created_at BETWEEN :from_date AND :to_date AND data_pass_id=:data_pass_id
    AND customer_id IN (SELECT id FROM {data_table} WHERE pda_url = :pda_url);
"""


class ScanTransactionsRepository(BaseRepository):
    async def create_scan_transaction(
        self, *, scan_transaction: Union[ScanTransactionNew, ScanTransactionNewTest]
    ) -> Optional[ScanTransactionBasicView]:
        query_values = scan_transaction.dict()
        query = (
            NEW_SCAN_TRANSACTION_SQL
            if isinstance(scan_transaction, ScanTransactionNew)
            else NEW_SCAN_TRANSACTION_TEST_SQL_
        )
        created_scan_transaction = await self.db.fetch_one(
            query=query, values=query_values
        )

        return (
            None
            if created_scan_transaction is None
            else ScanTransactionBasicView(**created_scan_transaction)
        )

    async def get_scan_trans_count_with_interval_n_days(
        self, *, interval_days: int, user_id: uuid.UUID, data_pass_id: uuid.UUID
    ) -> ScanTransactionCounts:
        now = datetime.now()
        first_from_date = (now - timedelta(days=interval_days)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        second_from_date = first_from_date - timedelta(days=interval_days)
        third_from_date = second_from_date - timedelta(days=interval_days)

        first_transaction = await self.db.fetch_one(
            query=GET_SCAN_TRANSACTIONS_COUNT_SQL,
            values={
                "from_date": first_from_date,
                "to_date": now,
                "user_id": user_id,
                "data_pass_id": data_pass_id,
            },
        )

        second_transaction = await self.db.fetch_one(
            query=GET_SCAN_TRANSACTIONS_COUNT_SQL,
            values={
                "from_date": second_from_date,
                "to_date": first_from_date - timedelta(microseconds=1),
                "user_id": user_id,
                "data_pass_id": data_pass_id,
            },
        )

        third_transaction = await self.db.fetch_one(
            query=GET_SCAN_TRANSACTIONS_COUNT_SQL,
            values={
                "from_date": third_from_date,
                "to_date": second_from_date - timedelta(microseconds=1),
                "user_id": user_id,
                "data_pass_id": data_pass_id,
            },
        )
        return ScanTransactionCounts(
            interval_1=ScanTransactionCount(**first_transaction).compute(),
            interval_2=ScanTransactionCount(**second_transaction).compute(),
            interval_3=ScanTransactionCount(**third_transaction).compute(),
        )

    async def get_customer_scan_trans_count_with_interval_n_days(
        self, *, interval_days: int, pda_url: str, data_pass_id: uuid.UUID, data_table: str,
    ) -> ScanTransactionCounts:
        now = datetime.now()
        first_from_date = (now - timedelta(days=interval_days)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        second_from_date = first_from_date - timedelta(days=interval_days)
        third_from_date = second_from_date - timedelta(days=interval_days)
   
        first_transaction = await self.db.fetch_one(
            query=GET_CUSTOMER_SCAN_TRANSACTIONS_COUNT_SQL.format(data_table=data_table),
            values={
                "from_date": first_from_date,
                "to_date": now,
                "pda_url": pda_url,
                "data_pass_id": data_pass_id,
            },
        )

        second_transaction = await self.db.fetch_one(
            query=GET_CUSTOMER_SCAN_TRANSACTIONS_COUNT_SQL.format(data_table=data_table),
            values={
                "from_date": second_from_date,
                "to_date": first_from_date - timedelta(microseconds=1),
                "pda_url": pda_url,
                "data_pass_id": data_pass_id,
            },
        )

        third_transaction = await self.db.fetch_one(
            query=GET_CUSTOMER_SCAN_TRANSACTIONS_COUNT_SQL.format(data_table=data_table),
            values={
                "from_date": third_from_date,
                "to_date": second_from_date - timedelta(microseconds=1),
                "pda_url": pda_url,
                "data_pass_id": data_pass_id,
            },
        )
        return ScanTransactionCounts(
            interval_1=ScanTransactionCount(**first_transaction).compute(),
            interval_2=ScanTransactionCount(**second_transaction).compute(),
            interval_3=ScanTransactionCount(**third_transaction).compute(),
        )
