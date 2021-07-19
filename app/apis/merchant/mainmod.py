import uuid

from app.db.repositories.customers import CustomersRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.scan_transaction import ScanTransactionNew, ScanTransactionCount


async def fn_verify_barcode(barcode: str,
                            user_id: uuid.UUID,
                            customers_repo: CustomersRepository,
                            scan_transactions_repo: ScanTransactionsRepository) -> bool:
    try:
        barcode_str = uuid.UUID(barcode)
    except ValueError:
        barcode_str = None

    valid_uuid = barcode_str is not None

    customer = await customers_repo.get_customer(customer_id=barcode_str) if valid_uuid else None
    customer_id = None if customer is None else customer.id

    await scan_transactions_repo.create_scan_transaction(scan_transaction=ScanTransactionNew(
        customer_id=customer_id,
        user_id=user_id,
    ))

    return customer_id is not None


async def fn_get_scan_transactions_count(last_n_days: int,
                                         user_id: uuid.UUID,
                                         scan_transactions_repo: ScanTransactionsRepository) \
        -> ScanTransactionCount:
    return await scan_transactions_repo.get_scan_transactions_count_from_last_n_days(n=last_n_days, user_id=user_id)
