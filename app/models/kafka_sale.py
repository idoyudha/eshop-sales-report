import uuid

class KafkaSaleItemCreated:
    product_id: uuid.UUID
    quantity: int
    price: float

class KafkaSaleCreated:
    user_id: uuid.UUID 
    order_id: uuid.UUID
    items: list[KafkaSaleItemCreated]
