"""SQLAlchemy Base model with common fields."""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime
from datetime import datetime
from typing import Any

class Base(DeclarativeBase):
    """Base class for all models."""
    pass

class BaseModel(Base):
    """Base model with common timestamp fields."""
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
