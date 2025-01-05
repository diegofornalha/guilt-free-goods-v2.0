from prisma.client import Prisma
from fastapi import Depends
from typing import AsyncGenerator

db = Prisma()

async def init_db() -> None:
    """Initialize database connection."""
    await db.connect()

async def close_db() -> None:
    """Close database connection."""
    await db.disconnect()

async def get_db_dependency() -> AsyncGenerator[Prisma, None]:
    """Dependency for database access in FastAPI routes."""
    try:
        yield db
    finally:
        # Connection is managed by lifecycle events
        pass

def get_db() -> Prisma:
    """Direct database client access for background jobs."""
    return db

# For FastAPI dependency injection
get_db_for_route = Depends(get_db_dependency)
