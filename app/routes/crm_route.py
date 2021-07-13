import uuid
from typing import List, Union, Optional

from app import global_state
from app.apis.crm.mainmod import fn_get_customer, fn_list_customers, fn_customer_upload, fn_merchant_upload
from app.apis.dependencies.database import get_repository
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import CreatedCount, NotFound
from app.models.customer import CustomerView
from fastapi import APIRouter, Depends, UploadFile, File, Response, BackgroundTasks
from starlette.status import HTTP_201_CREATED

router = APIRouter()
router.prefix = "/api/crm"

crm_user = global_state.fastapi_users.current_user(active=True, verified=True, superuser=True)


@router.get("/customers", tags=["crm"], response_model=List[CustomerView])
async def list_customers(page: Optional[int] = 1,
                         page_count: Optional[int] = 20,
                         customers_repository: CustomersRepository = Depends(get_repository(CustomersRepository)),
                         auth=Depends(crm_user)) -> List[CustomerView]:
    return await fn_list_customers(page, page_count, customers_repository)


@router.get("/customers/{customer_id}", tags=["crm"],
            response_model=CustomerView,
            responses={404: {"model": NotFound}})
async def get_customer(customer_id: uuid.UUID,
                       response: Response,
                       customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
                       auth=Depends(crm_user)) -> Union[CustomerView, NotFound]:
    return await fn_get_customer(customer_id, customers_repo, response)


@router.post("/customers/upload", response_model=CreatedCount, tags=["crm"], status_code=HTTP_201_CREATED)
async def upload(customers_file: UploadFile = File(...),
                 customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
                 auth=Depends(crm_user)) -> CreatedCount:
    return await fn_customer_upload(customers_file, customers_repo)


@router.post("/merchants/upload", response_model=CreatedCount, tags=["crm"], status_code=HTTP_201_CREATED)
async def upload(background_tasks: BackgroundTasks,
                 merchants_file: UploadFile = File(...),
                 merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
                 auth=Depends(crm_user)) -> CreatedCount:
    return await fn_merchant_upload(merchants_file, merchants_repo, background_tasks)


@router.get("/merchants", tags=["crm"])
async def upload(merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
                 auth=Depends(crm_user)) -> List:
    return await merchants_repo.get_merchants_email_list()
