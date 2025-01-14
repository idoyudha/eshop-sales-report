from fastapi import APIRouter, Depends

router = APIRouter(prefix="/utils", tags=["utils"])

@router.get("/health")
async def healthcheck():
    return {"status": "ok"}