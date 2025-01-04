from prisma import Prisma

db = Prisma()

async def init_db() -> None:
    """Initialize database connection."""
    await db.connect()

async def close_db() -> None:
    """Close database connection."""
    await db.disconnect()
