from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID
from app.db.session import get_session
from app.models.sale import Sale, SaleRead

router = APIRouter()

@router.get("/", response_model=List[SaleRead])
async def read_sales(
    *,
    session: AsyncSession = Depends(get_session),
    product_id: Optional[UUID] = Query(None, description="Filter by product ID"),
    warehouse_id: Optional[UUID] = Query(None, description="Filter by warehouse ID"),
    user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
    order_id: Optional[UUID] = Query(None, description="Filter by order ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    query = select(Sale)

    # filters
    if product_id:
        query = query.where(Sale.product_id == product_id)
    if warehouse_id:
        query = query.where(Sale.warehouse_id == warehouse_id)
    if user_id:
        query = query.where(Sale.user_id == user_id)
    if order_id:
        query = query.where(Sale.order_id == order_id)

    # pagination
    query = query.offset(skip).limit(limit)

    result = await session.exec(query)
    sales = result.scalars().all()
    return sales