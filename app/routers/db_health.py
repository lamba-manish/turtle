from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel
from app.database.db import get_db, engine

router = APIRouter(tags=["health"])


class DBHealthResponse(BaseModel):
    status: str
    message: str
    request_id: str


@router.get("/db-health", response_model=DBHealthResponse)
async def db_health_check(request: Request):
    """
    Database health check endpoint to verify the database connection
    """
    try:
        # Use a direct connection to check database health
        async with engine.connect() as conn:
            # Execute a simple query to check if the database is accessible
            result = await conn.execute(text("SELECT 1"))
            row = result.scalar()
            
            if row == 1:
                return {
                    "status": "ok",
                    "message": "Database connection successful",
                    "request_id": request.state.request_id
                }
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Database connection failed: unexpected result"
                )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
