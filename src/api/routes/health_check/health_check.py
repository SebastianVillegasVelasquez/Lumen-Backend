from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db

router = APIRouter(prefix="/health-check", tags=["health-check"])


@router.get("/")
async def health_check() -> dict[str, str]:
    """
    Only test the API server's health without checking the database connection.
    """
    return {"status": "ok"}


@router.get("/db")
async def health_check_db(db: AsyncSession = Depends(get_db)):
    """
    Check the API server's health and database connectivity.
    """
    try:
        # Execute a simple query to check database connectivity
        await db.execute(text("SELECT 1"))
        return {"status": "online", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
