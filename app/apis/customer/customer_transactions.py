from app.models.data_pass_source import DataPassSourceDescriptor
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
import uuid

from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.scan_transaction import ScanTransactionCounts


async def fn_customer_get_scan_transactions_count(
    interval_days: int,
    pda_url: str,
    data_pass_id: uuid.UUID,
    data_pass_sources_repo: DataPassSourcesRepository,
    scan_transactions_repo: ScanTransactionsRepository,
) -> ScanTransactionCounts:
    data_descriptors: DataPassSourceDescriptor = (
        await data_pass_sources_repo.get_basic_data_pass_source_descriptors(
            data_pass_id=data_pass_id
        )
    )
    return (
        await scan_transactions_repo.get_customer_scan_trans_count_with_interval_n_days(
            interval_days=interval_days, pda_url=pda_url, data_pass_id=data_pass_id, data_table=data_descriptors
        )
    )
