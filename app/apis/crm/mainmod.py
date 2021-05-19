from typing import List, Union

from .uploadmod import do_file_upload
import uuid

from app.models.customer import CustomerView
from fastapi import UploadFile, Response, status

from app.db.repositories.customers import CustomersRepository
from app.models.core import CreatedCount, NotFound


async def fn_list_customers(page: int,
                            page_count: int,
                            customers_repo: CustomersRepository) -> List[CustomerView]:
    limit = page_count
    offset = (page-1) * page_count
    return await customers_repo.get_customers(offset=offset, limit=limit)


async def fn_get_customer(user_id: uuid.UUID,
                          customers_repo: CustomersRepository,
                          response: Response) -> Union[CustomerView, NotFound]:
    customer = await customers_repo.get_customer(customer_id=user_id)
    if customer is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Customer Not Found")
    return customer


async def fn_upload(file: UploadFile, customers_repo: CustomersRepository) -> CreatedCount:
    return await do_file_upload(file, customers_repo)
