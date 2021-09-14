import uuid
from typing import Union

from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from starlette.status import HTTP_201_CREATED

from app.apis.crm.mainmod import fn_customer_upload
from app.apis.dependencies.database import get_repository
from app.core.auth import current_supplier
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.models.core import CreatedCount
from app.models.data_pass import InvalidDataPass

router = APIRouter()
router.prefix = "/api/supplier"


@router.post(
    "/data/upload",
    name="supplier:upload_data",
    tags=["suppliers"],
    status_code=HTTP_201_CREATED,
    responses={201: {"model": CreatedCount}, 400: {"model": InvalidDataPass}},
)
async def upload_data(
    response: Response,
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    customers_file: UploadFile = File(...),
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
    auth=Depends(current_supplier),
) -> Union[CreatedCount, InvalidDataPass]:
    upload_count = await fn_customer_upload(
        data_pass_id, data_passes_repo, customers_file, customers_repo
    )
    if upload_count is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()

    return upload_count
