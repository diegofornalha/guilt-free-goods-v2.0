"""Listing model."""
from sqlalchemy import Column, String, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import BaseModel

class Listing(BaseModel):
    """Listing model for marketplace listings."""
    __tablename__ = 'listings'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    marketplace = Column(String, nullable=False)  # e.g., "ebay", "amazon"
    status = Column(String, nullable=True)  # e.g., "active", "sold", "draft"
    external_id = Column(String, nullable=True)  # ID on the marketplace platform
    price = Column(Numeric(10, 2), default=0.00, nullable=False)
    
    # Foreign keys
    item_id = Column(String, ForeignKey('items.id'), nullable=False)
    
    # Relationships
    item = relationship("Item", back_populates="listings")
    market_research = relationship("MarketResearchData", back_populates="listing")
    orders = relationship("Order", back_populates="listing")
    analytics = relationship("AnalyticsData", back_populates="listing")
    
    # Platform-specific data
    platform_data = Column(JSON, nullable=True)
    performance_metrics = Column(JSON, nullable=True)
