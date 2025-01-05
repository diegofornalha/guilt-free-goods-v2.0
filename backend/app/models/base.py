"""SQLAlchemy Base model with common fields."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime
from typing import Any

Base = declarative_base()

class BaseModel(Base):
    """Base model with common timestamp fields."""
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
