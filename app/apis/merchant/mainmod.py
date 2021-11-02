import uuid
from typing import List

from fastapi import Request

from app.apis.merchant import merchant_data_pass, merchant_merchant_offer
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
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
    data_pass_sources_repo: DataPassSourcesRepository,
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

    data_pass_source = (
        await data_pass_sources_repo.get_basic_data_pass_source_descriptors(
            data_pass_id=data_pass_id
        )
    )
    customer = (
        None
        if data_pass_source is None
        else (
            await customers_repo.get_customer(
                customer_id=barcode_str, data_table=data_pass_source.data_table
            )
            if valid_uuid
            else None
        )
    )
    customer_id = None if customer is None else customer.id
    customer_pda_url = None if customer is None else customer.pda_url

    is_valid_data_pass = False
    is_data_pass_expired = False
    if data_pass_ident is None or customer_pda_url is None:
        await scan_transactions_repo.create_scan_transaction(
            scan_transaction=ScanTransactionNew(
                customer_id=customer_id,
                user_id=user_id,
                data_pass_id=None,
                data_pass_verified_valid=False,
                data_pass_expired=False,
            )
        )
    else:
        is_data_pass_expired = await data_passes_repo.is_data_pass_expired(
            data_pass_id=data_pass_ident, pda_url=customer_pda_url
        )
        is_valid_data_pass = (
            False
            if is_data_pass_expired
            else await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_ident)
        )

        await scan_transactions_repo.create_scan_transaction(
            scan_transaction=ScanTransactionNew(
                customer_id=customer_id,
                user_id=user_id,
                data_pass_id=data_pass_ident if valid_uuid else None,
                data_pass_verified_valid=is_valid_data_pass,
                data_pass_expired=is_data_pass_expired,
            )
        )
        if not is_valid_data_pass:
            log.info("invalid-datapass({})".format(str(data_pass_ident)))
        if is_data_pass_expired:
            log.info(
                "expired-datapass({}):{}".format(str(data_pass_ident), customer_pda_url)
            )

    result = customer_id is not None
    log.info("{}:{}:{}:{}".format(barcode, data_pass_id, user_id, result))
    return (
        [
            customer_id,
            barcode_str,
            data_pass_ident,
            is_valid_data_pass,
            is_data_pass_expired,
        ]
        if raw
        else [result, is_valid_data_pass, is_data_pass_expired]
    )


async def fn_get_scan_transactions_count(
    interval_days: int,
    user_id: uuid.UUID,
    data_pass_id: uuid.UUID,
    scan_transactions_repo: ScanTransactionsRepository,
) -> ScanTransactionCounts:
    return await scan_transactions_repo.get_scan_trans_count_with_interval_n_days(
        interval_days=interval_days, user_id=user_id, data_pass_id=data_pass_id
    )


fn_get_merchant_data_passes = merchant_data_pass.fn_get_merchant_data_passes
fn_get_merchant_offers = merchant_merchant_offer.fn_get_merchant_offers
