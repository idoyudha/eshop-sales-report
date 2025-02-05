from http import HTTPStatus
from fastapi import APIRouter
from typing import Any

from app.api.deps import AsyncSessionDep
from app.models.sale import SalesPublic
from app.service.sale import get_sales_service, count_total_sales_service

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/", response_model=SalesPublic)
async def read_sales(
    session: AsyncSessionDep, 
    skip: int = 0, 
    limit: int = 10
) -> Any:
    """
    Retrieve sales.
    """
    count = await count_total_sales_service(session=session)
    sales = await get_sales_service(session=session, offset=skip, limit=limit)
    return SalesPublic(
        code=HTTPStatus.OK,
        data=sales, 
        count=count,
        message="success get"
    )