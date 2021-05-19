from typing import Union, Optional, List

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, Response

from app.apis.customer.mainmod import fn_get_customer_basic, fn_search_customers, fn_claim_data
from app.core.pda_auth import get_current_pda_user
from app.apis.dependencies.database import get_repository
from app.db.repositories.customers import CustomersRepository
from app.models.core import NotFound
from app.models.customer import CustomerBasicView, CustomerView, CustomerSearch, CustomerClaim, CustomerClaimResponse

router = APIRouter()


# Authentication
@router.get("/auth/callback", tags=["authentication"])
async def callback(token: str) -> RedirectResponse:
    return RedirectResponse('/#/pages/customer/basic?token={}'.format(token))


@router.get("/customer/basic", tags=["customer"])
async def get_customer_basic(response: Response,
                             customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                             auth=Depends(get_current_pda_user)) -> Union[CustomerBasicView, NotFound]:
    return await fn_get_customer_basic(auth['iss'], customers_repository, response)


@router.post("/customer/search", tags=["customer"])
async def search_customers(search_params: CustomerSearch,
                           customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                           auth=Depends(get_current_pda_user)) -> List[CustomerView]:
    return await fn_search_customers(search_params.last_name,
                                     search_params.house_number,
                                     search_params.email,
                                     customers_repository)


@router.post("/customer/claim", tags=["customer"])
async def search_customers(claim_params: CustomerClaim,
                           response: Response,
                           customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                           auth=Depends(get_current_pda_user)) -> Union[CustomerClaimResponse, NotFound]:
    return await fn_claim_data(claim_params.id, auth['iss'], customers_repository, response)
