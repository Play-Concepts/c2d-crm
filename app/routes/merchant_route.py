import uuid
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, File, Request, Response, UploadFile
from starlette.status import HTTP_201_CREATED

from app.apis.dependencies.database import get_repository
from app.apis.log.mainmod import (fn_log_merchant_activity,
                                  fn_merchant_get_log_activity_daily_stats)
from app.apis.merchant.mainmod import (fn_create_merchant_offer,
                                       fn_get_merchant_data_passes,
                                       fn_get_merchant_offers,
                                       fn_get_scan_transactions_count,
                                       fn_update_merchant_offer,
                                       fn_update_merchant_offer_status,
                                       fn_upload_merchant_offer_image,
                                       fn_verify_barcode)
from app.core import global_state
from app.db.repositories.activity_log import ActivityLogRepository
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchant_log import MerchantLogRepository
from app.db.repositories.merchant_offers import MerchantOffersRepository
from app.db.repositories.merchants import MerchantsRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.core import (DaySeriesUnit, NewRecordResponse, NotFound,
                             UpdatedRecordResponse)
from app.models.data_pass import DataPassMerchantView, InvalidDataPass
from app.models.merchant_offer import (ForbiddenMerchantOfferAccess,
                                       MerchantOfferMerchantView,
                                       MerchantOfferNewRequest,
                                       MerchantOfferUpdateRequest)
from app.models.scan_transaction import (ScanRequest, ScanResult,
                                         ScanTransactionCounts)

router = APIRouter()
router.prefix = "/api/merchant"

merchant_user = global_state.fastapi_users.current_user(
    active=True, verified=True, superuser=False
)


@router.post(
    "/data-passes/{data_pass_id}/barcode/verify",
    name="merchant:barcode_verify",
    tags=["merchants"],
    response_model=Union[ScanResult, InvalidDataPass],
)
@router.post(
    "/{data_pass_id}/barcode/verify",
    name="merchant:barcode_verify",
    tags=["merchants"],
    response_model=Union[ScanResult, InvalidDataPass],
    deprecated=True,
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
    data_pass_sources_repo: DataPassSourcesRepository = Depends(
        get_repository(DataPassSourcesRepository)
    ),
    auth=Depends(merchant_user),
) -> Union[ScanResult, InvalidDataPass]:
    verified, is_valid_data_pass, is_data_pass_expired = await fn_verify_barcode(
        scan_request.barcode,
        data_pass_id,
        auth.id,
        customers_repo,
        scan_transactions_repo,
        data_passes_repo,
        data_pass_sources_repo,
        request=request,
    )
    return (
        ScanResult(verified=verified, message="")
        if is_valid_data_pass
        else InvalidDataPass(expired=is_data_pass_expired)
    )


@router.get(
    "/data-passes/{data_pass_id}/scan-transactions-count",
    name="merchant:scan-transactions-count",
    tags=["merchants"],
    response_model=ScanTransactionCounts,
)
@router.get(
    "/{data_pass_id}/scan-transactions-count",
    name="merchant:scan-transactions-count",
    tags=["merchants"],
    response_model=ScanTransactionCounts,
    deprecated=True,
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
    auth=Depends(merchant_user),
) -> List[DataPassMerchantView]:
    return await fn_get_merchant_data_passes(data_passes_repository)


@router.get(
    "/offers",
    name="merchant:offers",
    tags=["merchants"],
    response_model=List[MerchantOfferMerchantView],
)
async def get_merchant_offers(
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    auth=Depends(merchant_user),
) -> List[MerchantOfferMerchantView]:
    return await fn_get_merchant_offers(
        auth.email,
        merchant_offers_repo,
    )


@router.post(
    "/offers",
    name="merchant:offers:create",
    tags=["merchants"],
    status_code=HTTP_201_CREATED,
    responses={
        201: {"model": Optional[NewRecordResponse]},
        404: {"model": NotFound},
    },
)
async def create_merchant_offer(
    response: Response,
    merchant_offer_new_request: MerchantOfferNewRequest,
    merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    auth=Depends(merchant_user),
) -> Union[NotFound, Optional[NewRecordResponse]]:
    return await fn_create_merchant_offer(
        auth.email,
        merchant_offer_new_request,
        merchants_repo,
        merchant_offers_repo,
        response,
    )


@router.put(
    "/offers",
    name="merchant:offers:update",
    tags=["merchants"],
    responses={
        200: {"model": Optional[UpdatedRecordResponse]},
        403: {"model": ForbiddenMerchantOfferAccess},
        404: {"model": NotFound},
    },
)
async def update_merchant_offer(
    response: Response,
    merchant_offer_update_request: MerchantOfferUpdateRequest,
    merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    auth=Depends(merchant_user),
) -> Union[NotFound, ForbiddenMerchantOfferAccess, Optional[UpdatedRecordResponse]]:
    return await fn_update_merchant_offer(
        auth.email,
        merchant_offer_update_request,
        merchants_repo,
        merchant_offers_repo,
        response,
    )


@router.post(
    "/offers/{merchant_offer_id}/upload",
    name="merchant:offers:upload_image",
    tags=["merchants"],
)
async def upload_merchant_offer_image(
    response: Response,
    merchant_offer_id: uuid.UUID,
    image_file: UploadFile = File(...),
    merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    auth=Depends(merchant_user),
) -> int:
    return await fn_upload_merchant_offer_image(
        auth.email,
        merchant_offer_id,
        image_file,
        merchants_repo,
        merchant_offers_repo,
        response,
    )


@router.put(
    "/offers/{merchant_offer_id}/update-status/{status}",
    name="merchant:offers:update_status",
    tags=["merchants"],
    responses={
        200: {"model": Optional[UpdatedRecordResponse]},
        403: {"model": ForbiddenMerchantOfferAccess},
        404: {"model": NotFound},
    },
)
async def update_merchant_offer_status(
    response: Response,
    merchant_offer_id: uuid.UUID,
    status: str,
    merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    auth=Depends(merchant_user),
) -> Union[NotFound, ForbiddenMerchantOfferAccess, Optional[UpdatedRecordResponse]]:
    return await fn_update_merchant_offer_status(
        auth.email,
        merchant_offer_id,
        status,
        merchants_repo,
        merchant_offers_repo,
        response,
    )


@router.put(
    "/events/{component}/{component_identifier}/{event}",
    name="merchant:event:update_log",
    tags=["merchants", "logs"],
    response_model=NewRecordResponse,
)
async def log_activity(
    component: str,
    component_identifier: uuid.UUID,
    event: str,
    merchant_log_repo: MerchantLogRepository = Depends(
        get_repository(MerchantLogRepository)
    ),
    auth=Depends(merchant_user),
) -> NewRecordResponse:
    return await fn_log_merchant_activity(
        auth.id,
        component,
        component_identifier,
        event,
        merchant_log_repo,
    )


@router.get(
    "/events/{component}/{component_identifier}/{event}",
    name="merchant:event:log",
    tags=["merchants", "logs"],
    responses={
        200: {"model": List[DaySeriesUnit]},
        403: {"model": ForbiddenMerchantOfferAccess},
        404: {"model": NotFound},
    },
)
async def merchant_get_log_activity_daily_stats(
    response: Response,
    component: str,
    component_identifier: uuid.UUID,
    event: str,
    days: int,
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    auth=Depends(merchant_user),
) -> Union[NotFound, ForbiddenMerchantOfferAccess, List[DaySeriesUnit]]:
    return await fn_merchant_get_log_activity_daily_stats(
        auth.email,
        days,
        component,
        component_identifier,
        event,
        activity_log_repo,
        merchants_repo,
        merchant_offers_repo,
        response,
    )
