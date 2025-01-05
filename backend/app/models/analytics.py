"""Analytics models."""
from sqlalchemy import Column, String, Integer, Float, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import BaseModel

class Analytics(BaseModel):
    """Analytics data model for listing performance."""
    __tablename__ = 'analytics_data'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    view_count = Column(Integer, default=0, nullable=False)
    click_count = Column(Integer, default=0, nullable=False)
    conversion_rate = Column(Float, nullable=True)
    revenue = Column(Numeric(10, 2), default=0.00, nullable=False)
    profit_margin = Column(Float, nullable=True)
    platform_metrics = Column(JSON, nullable=True)
    
    # Foreign keys
    listing_id = Column(String, ForeignKey('listings.id'), nullable=False)
    
    # Relationships
    listing = relationship("Listing", back_populates="analytics")
    
    # Timestamps from Prisma schema
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

class AnalyticsSnapshot(BaseModel):
    """Analytics snapshot model for aggregated metrics."""
    __tablename__ = 'analytics_snapshots'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    total_revenue = Column(Numeric(10, 2), default=0.00, nullable=False)
    total_profit = Column(Numeric(10, 2), default=0.00, nullable=False)
    top_categories = Column(JSON, nullable=True)
    platform_insights = Column(JSON, nullable=True)
    customer_metrics = Column(JSON, nullable=True)
    
    # Timestamps from Prisma schema
    date = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
