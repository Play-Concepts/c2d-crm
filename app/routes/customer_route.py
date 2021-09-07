import uuid
from typing import List, Union

from fastapi import APIRouter, Depends, Request, Response, status

from app.apis.customer.mainmod import (fn_check_first_login, fn_claim_data,
                                       fn_customer_activate_data_pass,
                                       fn_get_customer_basic,
                                       fn_get_customer_data_passes,
                                       fn_search_customers)
from app.apis.dependencies.database import get_repository
from app.core.pda_auth import get_current_pda_user
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.customers_log import CustomersLogRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.logger import log_instance
from app.models.core import BooleanResponse, IDModelMixin, NotFound
from app.models.customer import (CustomerBasicView, CustomerClaim,
                                 CustomerClaimResponse, CustomerSearch,
                                 CustomerView)
from app.models.data_pass import DataPassCustomerView, InvalidDataPass

router = APIRouter()
router.prefix = "/api/customer"


@router.get(
    "/basic",
    name="customer:basic",
    tags=["customer"],
    response_model=CustomerBasicView,
    responses={404: {"model": NotFound}},
)
async def get_customer_basic(
    response: Response,
    customers_repository: CustomersRepository = Depends(
        get_repository(CustomersRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> Union[CustomerBasicView, NotFound]:
    auth, _ = auth_tuple
    return await fn_get_customer_basic(auth["iss"], customers_repository, response)


@router.post(
    "/search",
    name="customer:search",
    tags=["customer"],
    response_model=List[CustomerView],
)
async def search_customers(
    search_params: CustomerSearch,
    customers_repository: CustomersRepository = Depends(
        get_repository(CustomersRepository)
    ),
    auth=Depends(get_current_pda_user),
) -> List[CustomerView]:
    return await fn_search_customers(
        search_params.last_name,
        search_params.house_number,
        search_params.email,
        customers_repository,
    )


@router.post(
    "/claim",
    name="customer:claim",
    tags=["customer"],
    response_model=CustomerClaimResponse,
    responses={404: {"model": NotFound}},
)
async def claim_data(
    claim_params: CustomerClaim,
    request: Request,
    response: Response,
    customers_repository: CustomersRepository = Depends(
        get_repository(CustomersRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> Union[CustomerClaimResponse, NotFound]:
    auth, token = auth_tuple
    result = await fn_claim_data(
        claim_params.id, auth["iss"], token, customers_repository, response
    )
    log = log_instance(request)
    if result is not None:
        log.info("customer:claim:{}:{}".format(claim_params.id, auth["iss"]))

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
    "/data-passes/{data_pass_id}/enable",
    name="customer:data-passes",
    tags=["customer"],
    response_model=IDModelMixin,
    responses={400: {"model": InvalidDataPass}},
)
async def activate_data_pass(
    response: Response,
    data_pass_id: uuid.UUID,
    data_passes_repository: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    auth_tuple=Depends(get_current_pda_user),
) -> Union[IDModelMixin, InvalidDataPass]:
    auth, _ = auth_tuple
    activation = await fn_customer_activate_data_pass(
        data_pass_id, auth["iss"], data_passes_repository
    )

    if activation is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()

    return activation
