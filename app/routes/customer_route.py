from typing import List, Union

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.apis.customer.mainmod import (fn_claim_data, fn_get_customer_basic,
                                       fn_search_customers, fn_check_first_login)
from app.apis.dependencies.database import get_repository
from app.core.pda_auth import get_current_pda_user
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.customers_log_repository import CustomersLogRepository
from app.models.core import NotFound, BooleanResponse
from app.models.customer import (CustomerBasicView, CustomerClaim,
                                 CustomerClaimResponse, CustomerSearch,
                                 CustomerView)

router = APIRouter()
router.prefix = "/api/customer"


@router.get("/basic", tags=["customer"], response_model=CustomerBasicView, responses={404: {"model": NotFound}})
async def get_customer_basic(response: Response,
                             customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                             auth_tuple=Depends(get_current_pda_user)) -> Union[CustomerBasicView, NotFound]:
    auth, _ = auth_tuple
    return await fn_get_customer_basic(auth['iss'], customers_repository, response)


@router.post("/search", tags=["customer"], response_model=List[CustomerView])
async def search_customers(search_params: CustomerSearch,
                           customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                           auth=Depends(get_current_pda_user)) -> List[CustomerView]:
    return await fn_search_customers(search_params.last_name,
                                     search_params.house_number,
                                     search_params.email,
                                     customers_repository)


@router.post("/claim",
             tags=["customer"],
             response_model=CustomerClaimResponse,
             responses={404: {"model": NotFound}})
async def claim_data(claim_params: CustomerClaim,
                     response: Response,
                     customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                     auth_tuple=Depends(get_current_pda_user)) -> Union[CustomerClaimResponse, NotFound]:
    auth, token = auth_tuple
    return await fn_claim_data(claim_params.id, auth['iss'], token, customers_repository, response)


@router.get("/check-first-login", tags=["customer"], response_model=BooleanResponse)
async def check_first_login(customers_log_repository: CustomersLogRepository =
                             Depends(get_repository(CustomersLogRepository)),
                             auth_tuple=Depends(get_current_pda_user)) -> BooleanResponse:
    auth, _ = auth_tuple
    return await fn_check_first_login(auth['iss'], customers_log_repository)
