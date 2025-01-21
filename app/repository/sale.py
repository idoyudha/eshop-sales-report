from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func

from app.models.sale import SaleCreate, Sale, SalePublic

async def create_sale(*, session: AsyncSession, sale_in: SaleCreate) -> Sale:
    db_item = Sale.model_validate(sale_in)
    session.add(db_item)
    # session.commit()
    # session.refresh(db_item)
    await session.flush() # flush to only get id
    return db_item

async def get_sales(*, session: AsyncSession, offset: int, limit: int) -> list[SalePublic]:
    statement = (
        select(Sale)
        .offset(offset)
        .limit(limit)
    )
    result = await session.exec(statement)
    return result.all()
    # return session.exec(statement).all()

async def count_total_sales(*, session: AsyncSession) -> int:
    count_statement = (
        select(func.count())
        .select_from(Sale)
    )
    result = await session.exec(count_statement)
    return result.one()