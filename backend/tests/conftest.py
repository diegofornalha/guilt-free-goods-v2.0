"""Test configuration and fixtures."""
import pytest
import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.db import get_db

# Test database URL
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/gfg_test")

@pytest.fixture(scope="session")
def engine():
    """Create test database engine."""
    return create_async_engine(
        TEST_DATABASE_URL,
        echo=True
    )

@pytest.fixture(scope="session")
async def create_tables(engine):
    """Create all tables for testing."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture
async def db_session(engine, create_tables):
    """Create a fresh database session for a test."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session):
    """Create a test client with the test database session."""
    from fastapi.testclient import TestClient
    from ..app.main import app
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
