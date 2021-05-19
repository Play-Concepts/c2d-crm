from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, Response

from app.apis.customer.mainmod import fn_get_customer_basic
from app.core.pda_auth import get_current_pda_user
from app.apis.dependencies.database import get_repository
from app.db.repositories.customers import CustomersRepository
from app.models.core import NotFound
from app.models.customer import CustomerBasicView

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
