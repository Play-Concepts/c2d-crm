import uuid
from typing import List

from fastapi import Request

from app.apis.merchant import merchant_data_pass
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.logger import log_instance
from app.models.scan_transaction import (ScanTransactionCounts,
                                         ScanTransactionNew)


async def fn_verify_barcode(
    barcode: str,
    data_pass_id: uuid.UUID,
    user_id: uuid.UUID,
    customers_repo: CustomersRepository,
    scan_transactions_repo: ScanTransactionsRepository,
    data_passes_repo: DataPassesRepository,
    *,
    raw: bool = False,
    request: Request = None,
) -> List:
    log = log_instance(request)
    try:
        barcode_val, data_pass_str = barcode.split(":")
        barcode_str = uuid.UUID(barcode_val)
        data_pass_ident = uuid.UUID(data_pass_str)
    except ValueError:
        log.info("invalid-barcode({})".format(barcode))
        barcode_str = None
        data_pass_ident = None

    valid_uuid = barcode_str is not None and data_pass_id == data_pass_ident

    customer = (
        await customers_repo.get_customer(customer_id=barcode_str)
        if valid_uuid
        else None
    )
    customer_id = None if customer is None else customer.id

    is_valid_data_pass = (
        False
        if data_pass_ident is None
        else await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_ident)
    )
    if is_valid_data_pass:
        await scan_transactions_repo.create_scan_transaction(
            scan_transaction=ScanTransactionNew(
                customer_id=customer_id,
                user_id=user_id,
                data_pass_id=data_pass_ident if valid_uuid else None,
            )
        )
    else:
        log.info("invalid-datapass({})".format(str(data_pass_ident)))

    result = customer_id is not None
    log.info("{}:{}:{}:{}".format(barcode, data_pass_id, user_id, result))
    return (
        [customer_id, barcode_str, data_pass_ident, is_valid_data_pass]
        if raw
        else [result, is_valid_data_pass]
    )


async def fn_get_scan_transactions_count(
    interval_days: int,
    user_id: uuid.UUID,
    data_pass_id: uuid.UUID,
    scan_transactions_repo: ScanTransactionsRepository,
) -> ScanTransactionCounts:
    return (
        await scan_transactions_repo.get_scan_transactions_count_with_interval_n_days(
            interval_days=interval_days, user_id=user_id, data_pass_id=data_pass_id
        )
    )


fn_get_merchant_data_passes = merchant_data_pass.fn_get_merchant_data_passes
