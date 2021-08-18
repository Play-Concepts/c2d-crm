from fastapi import APIRouter

router = APIRouter()
router.prefix = "/api"


@router.get("/", tags=["hello"], name="root:hello")
async def hello():
    return {}
