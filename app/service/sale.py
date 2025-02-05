from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.kafka_sale import KafkaSaleCreated
from app.models.sale import Sales
from app.utils.mapper import map_kafka_sale_to_sale
from app.repository.sale import create_sale, get_sales, count_total_sales
from app.utils.generate_xlsx import generate_xlsx

async def create_sale_service(session: AsyncSession, input: KafkaSaleCreated) -> list[Sales]:
    sales = map_kafka_sale_to_sale(input)
    result = []
    for sale in sales:
        result.append(await create_sale(session=session, sale_in=sale))
    return result

async def get_sales_service(session: AsyncSession, offset: int, limit: int) -> list[Sales]:
    return await get_sales(session=session, offset=offset, limit=limit)

async def count_total_sales_service(session: AsyncSession) -> int:
    return await count_total_sales(session=session)

async def generate_sales_report_xlsx_service(session: AsyncSession):
    sales = await get_sales(session=session, offset=0, limit=None)
    return generate_xlsx(sales)