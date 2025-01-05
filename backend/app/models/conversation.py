"""Conversation models."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel

class Conversation(BaseModel):
    """Conversation model for customer interactions."""
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation")

class Message(BaseModel):
    """Message model for conversation content."""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    
    # Foreign keys
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
