from pydantic import BaseModel, UUID5
from datetime import datetime

class SaleBase(BaseModel):
    warehouse_id: UUID5
    user_id: UUID5
    order_id: UUID5
    product_id: UUID5
    product_quantity: float
    margin_per_product: float
    margin: float

class Sale(SaleBase):
    id: UUID5
    created_at: datetime

    class Config:
        from_attributes = True