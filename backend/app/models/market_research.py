"""Market Research model."""
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import BaseModel

class MarketResearchData(BaseModel):
    """Market research data model."""
    __tablename__ = 'market_research_data'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    price_trend = Column(JSON, nullable=True)
    competitor_prices = Column(JSON, nullable=True)
    demand_metrics = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    
    # Foreign keys
    listing_id = Column(String, ForeignKey('listings.id'), nullable=False)
    
    # Relationships
    listing = relationship("Listing", back_populates="market_research")
