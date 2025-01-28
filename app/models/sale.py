import uuid
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, DateTime

# shared properties
class SaleBase(SQLModel):
    user_id: uuid.UUID = Field(index=True)
    order_id: uuid.UUID = Field(index=True)
    product_id: uuid.UUID = Field(index=True)
    product_quantity: int
    margin_per_product: float
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc)
    )

# database model, database table inferred from the class name
class Sales(SaleBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

# properties to receive on sale creation
class SaleCreate(SaleBase):
    pass

# properties to return via API, some fields are always required
class SalePublic(SaleBase):
    pass

class SalesPublic(SQLModel):
    code: int
    data: list[SalePublic]
    count: int
    message: str