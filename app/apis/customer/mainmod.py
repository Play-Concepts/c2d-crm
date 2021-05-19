from typing import Union
from fastapi import Response, status

from app.db.repositories.customers import CustomersRepository
from app.models.core import NotFound
from app.models.customer import CustomerBasicView


async def fn_get_customer_basic(pda_url: str,
                                customers_repo: CustomersRepository,
                                response: Response) -> Union[CustomerBasicView, NotFound]:
    customer = await customers_repo.get_customer_basic(pda_url=pda_url)
    if customer is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Customer Not Found")
    return customer
