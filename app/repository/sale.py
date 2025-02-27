from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func

from app.models.sale import SaleCreate, Sales, SalePublic

async def create_sale(*, session: AsyncSession, sale_in: SaleCreate) -> Sales:
    db_item = Sales.model_validate(sale_in)
    session.add(db_item)
    await session.flush() # flush to only get id
    return db_item

async def get_sales(*, session: AsyncSession, offset: int, limit: int) -> list[SalePublic]:
    statement = (
        select(Sales)
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(statement)
    sales = result.scalars().all()
    return [SalePublic.model_validate(sale) for sale in sales]

async def count_total_sales(*, session: AsyncSession) -> int:
    count_statement = select(func.count()).select_from(Sales)
    result = await session.execute(count_statement)
    return result.scalar()