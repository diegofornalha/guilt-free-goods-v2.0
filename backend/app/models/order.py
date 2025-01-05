"""Order model."""
from sqlalchemy import Column, String, Integer, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import BaseModel

class Order(BaseModel):
    """Order model for purchases."""
    __tablename__ = 'orders'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    quantity = Column(Integer, default=1, nullable=False)
    total_price = Column(Numeric(10, 2), default=0.00, nullable=False)
    status = Column(String, nullable=False)  # e.g., "pending", "shipped", "delivered"
    buyer_details = Column(JSON, nullable=True)
    
    # Foreign keys
    listing_id = Column(String, ForeignKey('listings.id'), nullable=False)
    
    # Relationships
    listing = relationship("Listing", back_populates="orders")
    shipment = relationship("Shipment", back_populates="order", uselist=False)
