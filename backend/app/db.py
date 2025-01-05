from prisma import Prisma
from fastapi import Depends

db = Prisma()

async def init_db() -> None:
    """Initialize database connection."""
    await db.connect()

async def close_db() -> None:
    """Close database connection."""
    await db.disconnect()

async def get_db():
    """Dependency for database access."""
    try:
        yield db
    finally:
        # Connection is managed by lifecycle events
        pass
