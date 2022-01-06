import uuid
from typing import List, Union

from fastapi import APIRouter, Body, Depends, Request, Response, status

from app.apis.customer.customer_merchant_offer import \
    fn_get_all_customer_offers
from app.apis.customer.mainmod import (fn_check_first_login, fn_claim_data,
                                       fn_customer_activate_data_pass,
                                       fn_customer_get_scan_transactions_count,
                                       fn_get_customer_data_passes,
                                       fn_get_customer_favourited_offers,
                                       fn_get_customer_offers,
                                       fn_like_merchant_offer,
                                       fn_search_customers,
                                       fn_unlike_merchant_offer)
from app.apis.dependencies.database import get_repository
from app.apis.log.mainmod import (fn_log_activity, fn_log_data_pass_activated,
                                  fn_log_offer_liked, fn_log_offer_unliked)
from app.core.pda_auth import get_current_pda_user
from app.db.repositories.activity_log import ActivityLogRepository
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.customers_log import CustomersLogRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchant_offers import MerchantOffersRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.logger import log_instance
from app.models.core import (BooleanResponse, IDModelMixin, NewRecordResponse,
                             NotFound)
from app.models.customer import (CustomerClaim, CustomerClaimResponse,
                                 CustomerView)
from app.models.data_pass import DataPassCustomerView, InvalidDataPass
from app.models.merchant_offer import MerchantOfferCustomerView
from app.models.scan_transaction import ScanTransactionCounts

router = APIRouter()
router.prefix = "/api/customer"


@router.post(
    "/data/{data_pass_id}/search",
    name="customer:search",
    tags=["customer"],
    response_model=List[CustomerView],
)
async def search_customers(
    request: Request,
    response: Response,
    data_pass_id: uuid.UUID,
    search_params: dict = Body(...),
    data_passes_repo: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    data_pass_sources_repo: DataPassSourcesRepository = Depends(
        get_repository(DataPassSourcesRepository)
    ),
    customers_repository: CustomersRepository = Depends(
        get_repository(CustomersRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> List[CustomerView]:
    return await fn_search_customers(
        data_pass_id,
        search_params,
        data_passes_repo,
        data_pass_sources_repo,
        customers_repository,
        request=request,
        response=response,
    )


@router.post(
    "/data/{data_pass_id}/claim",
    name="customer:claim",
    tags=["customer"],
    responses={
        200: {"model": CustomerClaimResponse},
        404: {"model": NotFound},
        400: {"model": InvalidDataPass},
    },
)
async def claim_data(
    data_pass_id: uuid.UUID,
    claim_params: CustomerClaim,
    request: Request,
    response: Response,
    data_passes_repository: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    data_pass_sources_repository: DataPassSourcesRepository = Depends(
        get_repository(DataPassSourcesRepository)
    ),
    customers_repository: CustomersRepository = Depends(
        get_repository(CustomersRepository)
    ),
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> Union[CustomerClaimResponse, NotFound, InvalidDataPass]:
    auth, token = auth_tuple
    result = await fn_claim_data(
        data_pass_id,
        claim_params.id,
        auth["iss"],
        token,
        data_passes_repository,
        data_pass_sources_repository,
        customers_repository,
        response,
    )
    log = log_instance(request)
    if result is not None and response.status_code not in [
        status.HTTP_404_NOT_FOUND,
        status.HTTP_400_BAD_REQUEST,
    ]:
        log.info(
            "customer:claim:{}:{}:{}".format(
                claim_params.id, result.data_table, auth["iss"]
            )
        )
        await fn_customer_activate_data_pass(
            data_pass_id, auth["iss"], data_passes_repository
        )

        await fn_log_data_pass_activated(data_pass_id, activity_log_repo)

    return result


@router.get(
    "/check-first-login",
    name="customer:check-first-login",
    tags=["customer"],
    response_model=BooleanResponse,
)
async def check_first_login(
    request: Request,
    customers_log_repository: CustomersLogRepository = Depends(
        get_repository(CustomersLogRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> BooleanResponse:
    auth, _ = auth_tuple
    is_first_login_response: BooleanResponse = await fn_check_first_login(
        auth["iss"], customers_log_repository
    )
    log = log_instance(request)
    if is_first_login_response.value:
        log.info("customer:first-login:{}".format(auth["iss"]))
    else:
        log.info("customer:signi:{}".format(auth["iss"]))
    return is_first_login_response


@router.get(
    "/data-passes",
    name="customer:data-passes",
    tags=["customer"],
    response_model=List[DataPassCustomerView],
)
async def get_customer_data_passes(
    data_passes_repository: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> List[DataPassCustomerView]:
    auth, _ = auth_tuple
    return await fn_get_customer_data_passes(auth["iss"], data_passes_repository)


@router.get(
    "/data-passes/{data_pass_id}/scan-transactions-count",
    name="customer:scan-transactions-count",
    tags=["customer"],
    response_model=ScanTransactionCounts,
)
async def get_scan_transactions_count(
    data_pass_id: uuid.UUID,
    interval_days: int,
    data_pass_sources_repo: DataPassSourcesRepository = Depends(
        get_repository(DataPassSourcesRepository)
    ),
    scan_transactions_repo: ScanTransactionsRepository = Depends(
        get_repository(ScanTransactionsRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> ScanTransactionCounts:
    auth, _ = auth_tuple
    return await fn_customer_get_scan_transactions_count(
        interval_days,
        auth["iss"],
        data_pass_id,
        data_pass_sources_repo,
        scan_transactions_repo,
    )


@router.get(
    "/data-passes/{data_pass_id}/offers",
    name="customer:offers",
    tags=["customer"],
    response_model=List[MerchantOfferCustomerView],
    responses={400: {"model": InvalidDataPass}},
)
async def get_customer_offers(
    response: Response,
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> Union[InvalidDataPass, List[MerchantOfferCustomerView]]:
    auth, _ = auth_tuple
    return await fn_get_customer_offers(
        data_pass_id,
        data_passes_repo,
        merchant_offers_repo,
        response,
    )


@router.put(
    "/events/{component}/{component_identifier}/{event}",
    name="customer:event:log",
    tags=["customer", "logs"],
    response_model=NewRecordResponse,
)
async def log_activity(
    component: str,
    component_identifier: uuid.UUID,
    event: str,
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    _=Depends(get_current_pda_user),
) -> NewRecordResponse:
    return await fn_log_activity(
        component,
        component_identifier,
        event,
        activity_log_repo,
    )


@router.put(
    "/offers/{merchant_offer_id}/like",
    name="customer:offers:like",
    tags=["customer"],
    response_model=IDModelMixin,
)
async def like_merchant_offer(
    merchant_offer_id: uuid.UUID,
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> IDModelMixin:
    auth, _ = auth_tuple
    favorite = await fn_like_merchant_offer(
        auth["iss"],
        merchant_offer_id,
        merchant_offers_repo,
    )
    await fn_log_offer_liked(
        merchant_offer_id,
        activity_log_repo,
    )
    return favorite


@router.put(
    "/offers/{merchant_offer_id}/unlike",
    name="customer:offers:unlike",
    tags=["customer"],
    response_model=IDModelMixin,
)
async def unlike_merchant_offer(
    merchant_offer_id: uuid.UUID,
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> IDModelMixin:
    auth, _ = auth_tuple
    puke = await fn_unlike_merchant_offer(
        auth["iss"],
        merchant_offer_id,
        merchant_offers_repo,
    )
    await fn_log_offer_unliked(
        merchant_offer_id,
        activity_log_repo,
    )
    return puke


@router.get(
    "/offers",
    name="customer:offers",
    tags=["customer"],
    response_model=List[MerchantOfferCustomerView],
)
async def get_all_customer_offers(
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    _=Depends(get_current_pda_user),
) -> List[MerchantOfferCustomerView]:
    return await fn_get_all_customer_offers(
        merchant_offers_repo,
    )


@router.get(
    "/offers/favourites",
    name="customer:offers:favourites",
    tags=["customer"],
    response_model=List[MerchantOfferCustomerView],
)
async def get_customer_favourited_offers(
    merchant_offers_repo: MerchantOffersRepository = Depends(
        get_repository(MerchantOffersRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> List[MerchantOfferCustomerView]:
    auth, _ = auth_tuple
    return await fn_get_customer_favourited_offers(
        auth["iss"],
        merchant_offers_repo,
    )
