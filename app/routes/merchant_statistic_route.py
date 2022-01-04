from fastapi import APIRouter

from app.core import global_state

router = APIRouter()
router.prefix = "/api/merchant/stats"

merchant_user = global_state.fastapi_users.current_user(
    active=True, verified=True, superuser=False
)


@router.post(
    "/data-passes/{data_pass_id}/population",
    name="merchant:data-pass:population",
    tags=["merchant-statistics"],
)
def get_data_pass_population():
    pass


@router.post(
    "/data-passes/{data_pass_id}/audience",
    name="merchant:data-pass:audience",
    tags=["merchant-statistics"],
)
def get_data_pass_audience():
    pass
