import uuid
from pydantic import BaseModel

class KafkaSaleItemCreated(BaseModel):
    product_id: uuid.UUID
    quantity: int
    price: float

class KafkaSaleCreated(BaseModel):
    user_id: uuid.UUID 
    order_id: uuid.UUID
    items: list[KafkaSaleItemCreated]
