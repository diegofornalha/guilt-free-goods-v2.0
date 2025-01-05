"""Item model."""
from sqlalchemy import Column, String, Float, JSON, ForeignKey, ARRAY, Numeric
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import BaseModel

class Item(BaseModel):
    """Item model representing goods for sale."""
    __tablename__ = 'items'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), default=0.00, nullable=False)
    condition = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    image_urls = Column(ARRAY(String), nullable=True)
    detection_score = Column(Float, nullable=True)
    
    # Foreign keys
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="items")
    listings = relationship("Listing", back_populates="item")
    
    # AI-related fields
    category_confidence = Column(Float, nullable=True)
    detected_category = Column(String, nullable=True)
    detected_brand = Column(String, nullable=True)
    quality_score = Column(Float, nullable=True)
    dimensions = Column(JSON, nullable=True)
    defects = Column(JSON, nullable=True)
