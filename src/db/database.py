"""Async database engine and session configuration."""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings

"""
Create an AsyncEngine instance and a AsyncSessionLocal instance.
The AsyncEngine instance is used to create a connection to the database, 
and the AsyncSessionLocal instance is used to create a session for the database operations.
"""

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session.

    Yields:
        AsyncSession: A database session for async operations.
    """
    async with AsyncSessionLocal() as session:
        yield session
