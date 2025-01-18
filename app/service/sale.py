from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.kafka_sale import KafkaSaleCreated
from app.models.sale import Sale
from app.utils.mapper import map_kafka_sale_to_sale
from app.repository.sale import create_sale

def create_sale_service(session: AsyncSession, input: KafkaSaleCreated) -> list[Sale]:
    sales = map_kafka_sale_to_sale(input)
    # TODO: can we improve become only one insert query?
    result = []
    for sale in sales:
        result.append(create_sale(session=session, sale_in=sale))
    return result