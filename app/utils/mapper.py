from app.models.kafka_sale import KafkaSaleCreated, KafkaSaleItemCreated
from app.models.sale import SaleCreate
from app.constants import margin

def map_kafka_sale_to_sale(kafka_sale: KafkaSaleCreated) -> list[SaleCreate]:
    sales = []
    for item in kafka_sale.items:
        sales.append(SaleCreate(
            user_id=kafka_sale.user_id,
            order_id=kafka_sale.order_id,
            product_id=item.product_id,
            product_quantity=item.quantity,
            margin_per_product=item.price * margin.MARGIN_PERCENTAGE_DEFAULT
        ))
    return sales