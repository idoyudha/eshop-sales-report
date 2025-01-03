from pydantic import BaseModel, UUID5

class SaleBase(BaseModel):
    warehouse_id: UUID5
    user_id: UUID5
    order_id: UUID5
    product_id: UUID5
    product_quantity: float
    margin_per_product: float
    margin: float