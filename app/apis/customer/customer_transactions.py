import uuid

from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.scan_transaction import ScanTransactionCounts


async def fn_customer_get_scan_transactions_count(
    interval_days: int,
    pda_url: str,
    data_pass_id: uuid.UUID,
    scan_transactions_repo: ScanTransactionsRepository,
) -> ScanTransactionCounts:
    return (
        await scan_transactions_repo.get_customer_scan_trans_count_with_interval_n_days(
            interval_days=interval_days, pda_url=pda_url, data_pass_id=data_pass_id
        )
    )
