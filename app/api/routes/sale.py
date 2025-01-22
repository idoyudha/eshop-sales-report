from http import HTTPStatus
from fastapi import APIRouter
from typing import Any

from app.api.deps import AsyncSessionDep
from app.models.sale import SalesPublic
from app.repository.sale import count_total_sales, get_sales

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
    count = await count_total_sales(session=session)
    sales = await get_sales(session=session, offset=skip, limit=limit)
    return SalesPublic(
        code=HTTPStatus.OK,
        data=sales, 
        count=count,
        message="success get"
    )