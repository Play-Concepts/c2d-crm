from fastapi import APIRouter, Request

from app.logger import log_instance

router = APIRouter()
router.prefix = "/api"


@router.get("/", tags=["hello"], name="root:hello")
async def hello(request: Request):
    log = log_instance(request)
    log.info("hello")
    return {}

@router.get("/sentry", tags=["hello"], name="root:sentry")
async def sentry(request: Request):
    log = log_instance(request)
    raise ValueError("Raising an error to test sentry - {}")
    return {}
