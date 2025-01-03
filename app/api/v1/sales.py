from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from app.schemas.sale import Sale
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[Sale])
async def read_sales(
    warehouse_id: Optional[UUID] = Query(None, description="Filter by warehouse_id"),
    user_id: Optional[UUID] = Query(None, description="Filter by user_id"),
    order_id: Optional[UUID] = Query(None, description="Filter by order_id"),
    product_id: Optional[UUID] = Query(None, description="Filter by product_id"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of items per page"),
    db: AsyncSession = Depends(get_db)
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
    query = query.limit(page_size).offset((page - 1) * page_size)

    async with db as session:
        result = await session.execute(query)
        sales = result.scalars().all()
        return sales