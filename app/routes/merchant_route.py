import uuid
from typing import List, Union

from fastapi import APIRouter, Depends, Request

from app.apis.dependencies.database import get_repository
from app.apis.merchant.mainmod import (fn_get_merchant_data_passes,
                                       fn_get_scan_transactions_count,
                                       fn_verify_barcode)
from app.core import global_state
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.data_pass import DataPassMerchantView, InvalidDataPass
from app.models.scan_transaction import (ScanRequest, ScanResult,
                                         ScanTransactionCounts)

router = APIRouter()
router.prefix = "/api/merchant"

merchant_user = global_state.fastapi_users.current_user(
    active=True, verified=True, superuser=False
)


@router.post(
    "/{data_pass_id}/barcode/verify",
    name="merchant:barcode_verify",
    tags=["merchants"],
    response_model=ScanResult,
)
async def verify_barcode(
    request: Request,
    data_pass_id: uuid.UUID,
    scan_request: ScanRequest,
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
    scan_transactions_repo: ScanTransactionsRepository = Depends(
        get_repository(ScanTransactionsRepository)
    ),
    data_passes_repo: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    auth=Depends(merchant_user),
) -> Union[ScanResult, InvalidDataPass]:
    verified, is_valid_data_pass = await fn_verify_barcode(
        scan_request.barcode,
        data_pass_id,
        auth.id,
        customers_repo,
        scan_transactions_repo,
        data_passes_repo,
        request=request,
    )
    if is_valid_data_pass:
        return ScanResult(verified=verified, str="")
    else:
        return InvalidDataPass()


@router.get(
    "/{data_pass_id}/scan-transactions-count",
    name="merchant:scan-transactions-count",
    tags=["merchants"],
    response_model=ScanTransactionCounts,
)
@router.get(
    "/{data_pass_id}/scan_transactions_count",
    name="merchant:scan_transactions_count",
    tags=["merchants"],
    response_model=ScanTransactionCounts,
    deprecated=True,
)
async def get_scan_transactions_count(
    data_pass_id: uuid.UUID,
    interval_days: int,
    scan_transactions_repo: ScanTransactionsRepository = Depends(
        get_repository(ScanTransactionsRepository)
    ),
    auth=Depends(merchant_user),
) -> ScanTransactionCounts:
    return await fn_get_scan_transactions_count(
        interval_days, auth.id, data_pass_id, scan_transactions_repo
    )


@router.get(
    "/data-passes",
    name="merchant:data-passes",
    tags=["merchants"],
    response_model=List[DataPassMerchantView],
)
async def get_customer_data_passes(
    data_passes_repository: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    auth_tuple=Depends(merchant_user),
) -> List[DataPassMerchantView]:
    return await fn_get_merchant_data_passes(data_passes_repository)
