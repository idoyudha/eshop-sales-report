from typing import Any

from fastapi import APIRouter
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models.sale import SalesPublic
from app.repository.sale import count_total_sales, get_sales

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/", response_model=SalesPublic)
def read_sales(
    session: SessionDep, skip: int = 0, limit: int = 10
) -> Any:
    """
    Retrieve sales.
    """
    count = count_total_sales(session=session)
    sales = get_sales(session=session, offset=skip, limit=limit)
    return SalesPublic(data=sales, count=count)