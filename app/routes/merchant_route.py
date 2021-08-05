from fastapi import APIRouter, Depends

from app.apis.dependencies.database import get_repository
from app.apis.merchant.mainmod import fn_get_scan_transactions_count, fn_verify_barcode
from app.core import global_state
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.scan_transaction import ScanRequest, ScanResult, ScanTransactionCounts

router = APIRouter()
router.prefix = "/api"

merchant_user = global_state.fastapi_users.current_user(
    active=True, verified=True, superuser=False
)


@router.post("/merchant/barcode/verify", name="merchant:barcode:verify", tags=["merchants"], response_model=ScanResult)
async def verify_barcode(
    request: ScanRequest,
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
    scan_transactions_repo: ScanTransactionsRepository = Depends(
        get_repository(ScanTransactionsRepository)
    ),
    auth=Depends(merchant_user),
) -> ScanResult:
    verified = await fn_verify_barcode(
        request.barcode, auth.id, customers_repo, scan_transactions_repo
    )
    return ScanResult(verified=verified)


@router.get(
    "/merchant/scan-transactions-count",
    name="merchant:scan-transactions-count",
    tags=["merchants"],
    response_model=ScanTransactionCounts,
)
@router.get(
    "/merchant/scan_transactions_count",
    name="merchant:scan_transactions_count",
    tags=["merchants"],
    response_model=ScanTransactionCounts,
    deprecated=True,
)
async def get_scan_transactions_count(
    interval_days: int,
    scan_transactions_repo: ScanTransactionsRepository = Depends(
        get_repository(ScanTransactionsRepository)
    ),
    auth=Depends(merchant_user),
) -> ScanTransactionCounts:
    return await fn_get_scan_transactions_count(
        interval_days, auth.id, scan_transactions_repo
    )
