from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import API_V1_STR, PROJECT_NAME
from app.middleware.logging import LoggingMiddleware
from app.routers import health, db_health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown events
    """
    # Startup event
    yield
    # Shutdown event


def create_application() -> FastAPI:
    """Create FastAPI application"""
    
    application = FastAPI(
        title=PROJECT_NAME,
        openapi_url=f"{API_V1_STR}/openapi.json",
        docs_url="/docs",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify the allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add logging middleware
    application.add_middleware(LoggingMiddleware)
    
    # Include routers
    application.include_router(health.router, prefix=API_V1_STR)
    application.include_router(db_health.router, prefix=API_V1_STR)
    
    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
