from fastapi import APIRouter

router = APIRouter()
router.prefix = "/api"


@router.get("/", tags=["hello"])
async def hello():
    return {"hello": "world"}
