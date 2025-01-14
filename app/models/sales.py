import uuid

from sqlmodel import Field, SQLModel

# shared properties
class SaleBase(SQLModel):
    warehouse_id: uuid.UUID = Field(index=True)
    user_id: uuid.UUID = Field(index=True)
    order_id: uuid.UUID = Field(index=True)
    product_id: uuid.UUID = Field(index=True)
    product_quantity: float

# properties to receive on sale creation
class SaleCreate(SaleBase):
    pass

class SalePublic(SaleBase):
    id: uuid.UUID
    margin_per_product: float
    created_at: str

class SalesPublic(SQLModel):
    data: list[SalePublic]
    count: int