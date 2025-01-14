from typing import Any

from fastapi import APIRouter
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models.sale import Sale, SalesPublic

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/", response_model=SalesPublic)
def read_sales(
    session: SessionDep, skip: int = 0, limit: int = 10
) -> Any:
    """
    Retrieve sales.
    """
    count_statement = (
        select(func.count())
        .select_from(Sale)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Sale)
        .offset(skip)
        .limit(limit)
    )
    sales = session.exec(statement).all()
    return SalesPublic(data=sales, count=count)