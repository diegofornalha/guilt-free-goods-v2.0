"""User model."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import BaseModel

class User(BaseModel):
    """User model for authentication and item ownership."""
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)

    # Relationships
    items = relationship("Item", back_populates="user")
