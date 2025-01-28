from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.kafka_sale import KafkaSaleCreated
from app.models.sale import Sales
from app.utils.mapper import map_kafka_sale_to_sale
from app.repository.sale import create_sale

async def create_sale_service(session: AsyncSession, input: KafkaSaleCreated) -> list[Sales]:
    sales = map_kafka_sale_to_sale(input)
    result = []
    for sale in sales:
        result.append(await create_sale(session=session, sale_in=sale))
    return result