from typing import List, Any

from app.apis.crm.mainmod import fn_get_customer, fn_list_customers, fn_upload
from app.apis.dependencies.database import get_repository
from app.db.repositories.customers import CustomersRepository
from app.models.core import CreatedCount
from app.models.customer import CustomerView, CustomerNew
from fastapi import APIRouter, Depends, UploadFile, File
from app.core.auth import get_current_user
from starlette.status import HTTP_201_CREATED

router = APIRouter()


@router.get("/crm/customers", tags=["crm"])
async def list_customers(auth=Depends(get_current_user)) -> List[CustomerView]:
    return fn_list_customers()


@router.get("/crm/customers/{customer_id}", tags=["crm"])
async def get_customer(customer_id: str, auth=Depends(get_current_user)) -> CustomerView:
    return fn_get_customer(customer_id)


@router.post("/crm/upload", response_model=CreatedCount, tags=["crm"], status_code=HTTP_201_CREATED)
async def upload(customers_file: UploadFile = File(...),
                 customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                 auth=Depends(get_current_user)) -> Any:
    return await fn_upload(customers_file, customers_repository)
