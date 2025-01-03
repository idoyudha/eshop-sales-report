from sqlalchemy import Column, Float, DateTime, UUID
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Sale(Base):
    __tablename__ = "sales_report"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid5)
    warehouse_id = Column(UUID, nullable=False, index=True)
    user_id = Column(UUID, nullable=False, index=True)
    order_id = Column(UUID, nullable=False, index=True)
    product_id = Column(UUID, nullable=False, index=True)
    product_quantity = Column(Float, nullable=False)
    margin_per_product = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())