import uuid
from typing import List, Union

from fastapi import APIRouter, Body, Depends, Request, Response

from app.apis.customer.mainmod import (fn_check_first_login, fn_claim_data,
                                       fn_customer_activate_data_pass,
                                       fn_customer_get_scan_transactions_count,
                                       fn_get_customer_basic,
                                       fn_get_customer_data_passes,
                                       fn_get_customer_favourited_perks,
                                       fn_get_customer_perks,
                                       fn_like_merchant_perk,
                                       fn_search_customers,
                                       fn_unlike_merchant_perk)
from app.apis.dependencies.database import get_repository
from app.apis.log.mainmod import (fn_log_data_pass_activated,
                                  fn_log_data_pass_info_view_entered,
                                  fn_log_data_pass_info_view_exited,
                                  fn_log_data_pass_perk_link_clicked,
                                  fn_log_perk_liked, fn_log_perk_unliked)
from app.core.pda_auth import get_current_pda_user
from app.db.repositories.activity_log import ActivityLogRepository
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.customers_log import CustomersLogRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchant_perks import MerchantPerksRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.logger import log_instance
from app.models.activity_log import ActivityLogNewResponse
from app.models.core import BooleanResponse, IDModelMixin, NotFound
from app.models.customer import (CustomerBasicView, CustomerClaim,
                                 CustomerClaimResponse, CustomerView)
from app.models.data_pass import DataPassCustomerView, InvalidDataPass
from app.models.merchant_perk import MerchantPerkCustomerView
from app.models.scan_transaction import ScanTransactionCounts

router = APIRouter()
router.prefix = "/api/customer"


@router.get(
    "/data/{data_pass_id}/basic",
    name="customer:basic",
    tags=["customer"],
    response_model=CustomerBasicView,
    responses={404: {"model": NotFound}, 400: {"model": InvalidDataPass}},
    deprecated=True,
)
async def get_customer_basic(
    response: Response,
    data_pass_id: uuid.UUID,
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
) -> Union[CustomerBasicView, NotFound, InvalidDataPass]:
    auth, _ = auth_tuple
    return await fn_get_customer_basic(
        data_pass_id,
        auth["iss"],
        data_passes_repo,
        data_pass_sources_repo,
        customers_repository,
        response,
    )


@router.post(
    "/data/{data_pass_id}/search",
    name="customer:search",
    tags=["customer"],
    response_model=List[CustomerView],
)
async def search_customers(
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
    auth=Depends(get_current_pda_user),
) -> List[CustomerView]:
    return await fn_search_customers(
        data_pass_id,
        search_params,
        data_passes_repo,
        data_pass_sources_repo,
        customers_repository,
        response,
    )


@router.post(
    "/data/{data_pass_id}/claim",
    name="customer:claim",
    tags=["customer"],
    response_model=CustomerClaimResponse,
    responses={404: {"model": NotFound}, 400: {"model": InvalidDataPass}},
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
    if result is not None:
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
@router.get(
    "/{data_pass_id}/scan-transactions-count",
    name="customer:scan-transactions-count",
    tags=["customer"],
    response_model=ScanTransactionCounts,
    deprecated=True,
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
    "/data-passes/{data_pass_id}/perks",
    name="customer:perks",
    tags=["customer"],
    response_model=List[MerchantPerkCustomerView],
    responses={400: {"model": InvalidDataPass}},
)
@router.get(
    "/{data_pass_id}/perks",
    name="customer:perks",
    tags=["customer"],
    response_model=List[MerchantPerkCustomerView],
    responses={400: {"model": InvalidDataPass}},
    deprecated=True,
)
async def get_customer_perks(
    response: Response,
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    merchant_perks_repo: MerchantPerksRepository = Depends(
        get_repository(MerchantPerksRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> Union[InvalidDataPass, List[MerchantPerkCustomerView]]:
    auth, _ = auth_tuple
    return await fn_get_customer_perks(
        auth["iss"],
        data_pass_id,
        data_passes_repo,
        merchant_perks_repo,
        response,
    )


@router.put(
    "/data-passes/{data_pass_id}/enter-info-view",
    name="customer:data-passes:enter-info-view",
    tags=["customer"],
    response_model=ActivityLogNewResponse,
)
async def log_data_pass_info_view_entered(
    data_pass_id: uuid.UUID,
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    _=Depends(get_current_pda_user),
) -> ActivityLogNewResponse:
    return await fn_log_data_pass_info_view_entered(
        data_pass_id,
        activity_log_repo,
    )


@router.put(
    "/data-passes/{data_pass_id}/exit-info-view",
    name="customer:data-passes:exit-info-view",
    tags=["customer"],
    response_model=ActivityLogNewResponse,
)
async def log_data_pass_info_view_exited(
    data_pass_id: uuid.UUID,
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    _=Depends(get_current_pda_user),
) -> ActivityLogNewResponse:
    return await fn_log_data_pass_info_view_exited(
        data_pass_id,
        activity_log_repo,
    )


@router.put(
    "/data-passes/{data_pass_id}/perk-link-clicked",
    name="customer:data-passes:perk-link-clicked",
    tags=["customer"],
    response_model=ActivityLogNewResponse,
)
async def log_data_pass_perk_link_clicked(
    data_pass_id: uuid.UUID,
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    _=Depends(get_current_pda_user),
) -> ActivityLogNewResponse:
    return await fn_log_data_pass_perk_link_clicked(
        data_pass_id,
        activity_log_repo,
    )


@router.put(
    "/perks/{merchant_perk_id}/like",
    name="customer:perks:like",
    tags=["customer"],
    response_model=IDModelMixin,
)
async def like_merchant_perk(
    merchant_perk_id: uuid.UUID,
    merchant_perks_repo: MerchantPerksRepository = Depends(
        get_repository(MerchantPerksRepository)
    ),
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> IDModelMixin:
    auth, _ = auth_tuple
    favorite = await fn_like_merchant_perk(
        auth["iss"],
        merchant_perk_id,
        merchant_perks_repo,
    )
    await fn_log_perk_liked(
        merchant_perk_id,
        activity_log_repo,
    )
    return favorite


@router.put(
    "/perks/{merchant_perk_id}/unlike",
    name="customer:perks:unlike",
    tags=["customer"],
    response_model=IDModelMixin,
)
async def unlike_merchant_perk(
    merchant_perk_id: uuid.UUID,
    merchant_perks_repo: MerchantPerksRepository = Depends(
        get_repository(MerchantPerksRepository)
    ),
    activity_log_repo: ActivityLogRepository = Depends(
        get_repository(ActivityLogRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> IDModelMixin:
    auth, _ = auth_tuple
    puke = await fn_unlike_merchant_perk(
        auth["iss"],
        merchant_perk_id,
        merchant_perks_repo,
    )
    await fn_log_perk_unliked(
        merchant_perk_id,
        activity_log_repo,
    )
    return puke


@router.get(
    "/perks",
    name="customer:perks",
    tags=["customer"],
    response_model=List[MerchantPerkCustomerView],
)
@router.get(
    "/perks/favourites",
    name="customer:perks:favourites",
    tags=["customer"],
    response_model=List[MerchantPerkCustomerView],
)
async def get_customer_favourited_perks(
    merchant_perks_repo: MerchantPerksRepository = Depends(
        get_repository(MerchantPerksRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> List[MerchantPerkCustomerView]:
    auth, _ = auth_tuple
    return await fn_get_customer_favourited_perks(
        auth["iss"],
        merchant_perks_repo,
    )
