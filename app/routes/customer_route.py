import uuid
from typing import List, Union

from fastapi import APIRouter, Body, Depends, Request, Response

from app.apis.customer.mainmod import (fn_check_first_login, fn_claim_data,
                                       fn_customer_activate_data_pass,
                                       fn_customer_get_scan_transactions_count,
                                       fn_get_customer_basic,
                                       fn_get_customer_data_passes,
                                       fn_search_customers)
from app.apis.dependencies.database import get_repository
from app.core.pda_auth import get_current_pda_user
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.customers_log import CustomersLogRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.logger import log_instance
from app.models.core import BooleanResponse, NotFound
from app.models.customer import (CustomerBasicView, CustomerClaim,
                                 CustomerClaimResponse, CustomerView)
from app.models.data_pass import DataPassCustomerView, InvalidDataPass
from app.models.scan_transaction import ScanTransactionCounts

router = APIRouter()
router.prefix = "/api/customer"


@router.get(
    "/data/{data_pass_id}/basic",
    name="customer:basic",
    tags=["customer"],
    response_model=CustomerBasicView,
    responses={404: {"model": NotFound}, 400: {"model": InvalidDataPass}},
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
    "/{data_pass_id}/scan-transactions-count",
    name="customer:scan-transactions-count",
    tags=["customer"],
    response_model=ScanTransactionCounts,
)
async def get_scan_transactions_count(
    data_pass_id: uuid.UUID,
    interval_days: int,
    scan_transactions_repo: ScanTransactionsRepository = Depends(
        get_repository(ScanTransactionsRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> ScanTransactionCounts:
    auth, _ = auth_tuple
    return await fn_customer_get_scan_transactions_count(
        interval_days, auth["iss"], data_pass_id, scan_transactions_repo
    )
