import uuid
from datetime import datetime

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

# database model, database table inferred from the class name
class Sale(SaleBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid5, primary_key=True)
    margin_per_product: float = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))

# properties to return via API, some fields are always required
class SalePublic(SaleBase):
    id: uuid.UUID
    margin_per_product: float
    created_at: datetime

class SalesPublic(SQLModel):
    data: list[SalePublic]
    count: int