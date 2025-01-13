from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from uuid import UUID, uuid5

class SaleBase(SQLModel):
    product_id: UUID = Field(index=True)
    warehouse_id: UUID = Field(index=True)
    user_id: UUID = Field(index=True)
    order_id: UUID = Field(index=True)
    margin: float

class Sale(SaleBase, table=True):
    __tablename__ = "sales_report"
    
    id: UUID = Field(
        default_factory=uuid5,
        primary_key=True,
        index=True,
    )
    created_at: datetime = Field(
        default_factory=datetime.now(timezone.utc),
        nullable=False,
    )

class SaleCreate(SaleBase):
    pass

class SaleRead(SaleBase):
    id: UUID
    created_at: datetime