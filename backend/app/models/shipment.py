"""Shipment model."""
from sqlalchemy import Column, String, Integer, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import BaseModel

class Shipment(BaseModel):
    """Shipment model for order fulfillment."""
    __tablename__ = 'shipments'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    carrier = Column(String, nullable=False)  # e.g., "AUS_POST"
    tracking_number = Column(String, nullable=True)
    status = Column(String, nullable=False)  # e.g., "PENDING", "SHIPPED"
    
    # Australia Post size limits
    weight = Column(Numeric(5, 2), nullable=True)  # in kg, max 22kg for domestic
    length = Column(Integer, nullable=True)  # in cm, max 105cm
    volume = Column(Numeric(5, 3), nullable=True)  # in cubic metres, max 0.25
    
    # Cost optimization fields
    shipping_cost = Column(Numeric(10, 2), default=0.00, nullable=False)
    quoted_costs = Column(JSON, nullable=True)
    selected_reason = Column(String, nullable=True)
    
    # Foreign keys
    order_id = Column(String, ForeignKey('orders.id'), unique=True, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="shipment")
