"""SQLAlchemy-based database client that provides a Prisma-like interface."""
from typing import Any, Dict, List, Optional, TypeVar, Generic, Type
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from .models.item import Item
from .models.user import User
from .models.listing import Listing
from .models.conversation import Conversation
from .models.order import Order
from .models.shipment import Shipment
from .models.analytics import Analytics
from .models.market_research import MarketResearchData

T = TypeVar('T')

class ModelClient(Generic[T]):
    """Generic model client providing Prisma-like operations."""
    
    def __init__(self, session: AsyncSession, model: Type[T]):
        """Initialize the model client."""
        self.session = session
        self.model = model
    
    async def create(self, data: Dict[str, Any]) -> T:
        """Create a new record."""
        instance = self.model(**data.get("data", {}))
        self.session.add(instance)
        await self.session.flush()
        return instance
    
    async def find_unique(self, where: Dict[str, Any]) -> Optional[T]:
        """Find a unique record."""
        stmt = select(self.model).filter_by(**where)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def find_many(self, skip: int = 0, take: int = 10, order: Optional[Dict[str, str]] = None) -> List[T]:
        """Find many records with pagination."""
        stmt = select(self.model)
        if order:
            for field, direction in order.items():
                column = getattr(self.model, field)
                stmt = stmt.order_by(column.desc() if direction == "desc" else column.asc())
        stmt = stmt.offset(skip).limit(take)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def update(self, where: Dict[str, Any], data: Dict[str, Any]) -> Optional[T]:
        """Update a record."""
        stmt = (
            update(self.model)
            .filter_by(**where)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def delete(self, where: Dict[str, Any]) -> Optional[T]:
        """Delete a record."""
        stmt = (
            delete(self.model)
            .filter_by(**where)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

class DatabaseClient:
    """Database client providing Prisma-like model access."""
    
    def __init__(self, session: AsyncSession):
        """Initialize the database client."""
        self.session = session
        self.item = ModelClient(session, Item)
        self.user = ModelClient(session, User)
        self.listing = ModelClient(session, Listing)
        self.conversation = ModelClient(session, Conversation)
        self.order = ModelClient(session, Order)
        self.shipment = ModelClient(session, Shipment)
        self.analytics = ModelClient(session, Analytics)
        self.market_research = ModelClient(session, MarketResearchData)

async def get_db_client(session: AsyncSession) -> DatabaseClient:
    """Create a database client from a session."""
    return DatabaseClient(session)
