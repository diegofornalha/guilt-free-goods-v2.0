"""Database connection and client management."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import AsyncGenerator
import os
from .db_client import DatabaseClient, get_db_client

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/gfg")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

# Create async session factory
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db() -> None:
    """Initialize database connection."""
    # SQLAlchemy creates connection pool automatically
    pass

async def close_db() -> None:
    """Close database connection."""
    await engine.dispose()

async def get_db_dependency() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for database access in FastAPI routes."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_db() -> AsyncSession:
    """Direct database client access for background jobs."""
    return async_session_factory()

# For FastAPI dependency injection
get_db_for_route = Depends(get_db_dependency)

# Create a db instance that mimics Prisma's interface
db = DatabaseClient(async_session_factory())
