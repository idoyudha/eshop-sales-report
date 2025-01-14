from fastapi import APIRouter, Depends

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def healthcheck():
    return {"status": "ok"}