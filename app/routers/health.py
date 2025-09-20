from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    request_id: str


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """
    Health check endpoint to verify the API is running
    """
    return {
        "status": "ok",
        "request_id": request.state.request_id
    }
