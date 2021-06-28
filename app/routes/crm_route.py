import uuid
from typing import List, Union, Optional

from app.apis.crm.mainmod import fn_get_customer, fn_list_customers, fn_upload
from app.apis.dependencies.database import get_repository
from app.db.repositories.customers import CustomersRepository
from app.models.core import CreatedCount, NotFound
from app.models.customer import CustomerView
from fastapi import APIRouter, Depends, UploadFile, File, Response
from app.core.auth import get_current_user
from starlette.status import HTTP_201_CREATED

router = APIRouter()


@router.get("/crm/customers", tags=["crm"], response_model=List[CustomerView])
async def list_customers(page: Optional[int] = 1,
                         page_count: Optional[int] = 20,
                         customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                         auth=Depends(get_current_user)) -> List[CustomerView]:
    return await fn_list_customers(page, page_count, customers_repository)


@router.get("/crm/customers/{customer_id}", tags=["crm"],
            response_model=CustomerView,
            responses={404: {"model": NotFound}})
async def get_customer(customer_id: uuid.UUID,
                       response: Response,
                       customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                       auth=Depends(get_current_user)) -> Union[CustomerView, NotFound]:
    return await fn_get_customer(customer_id, customers_repository, response)


@router.post("/crm/upload", response_model=CreatedCount, tags=["crm"], status_code=HTTP_201_CREATED)
async def upload(customers_file: UploadFile = File(...),
                 customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                 auth=Depends(get_current_user)) -> CreatedCount:
    return await fn_upload(customers_file, customers_repository)
