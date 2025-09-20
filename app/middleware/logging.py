import json
import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.config import LOG_LEVEL, LOG_DIR


# Configure loggers
def get_logger(name: str, log_file: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    
    # Set log level based on config
    level = getattr(logging, LOG_LEVEL)
    logger.setLevel(level)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(request_id)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    
    return logger


# Create loggers
info_logger = get_logger('info', LOG_DIR / 'info' / 'app.log')
error_logger = get_logger('error', LOG_DIR / 'error' / 'app.log')
request_logger = get_logger('request', LOG_DIR / 'request' / 'app.log')


class LoggingContextFilter(logging.Filter):
    """Add request_id to log records"""
    
    def __init__(self, request_id: str):
        super().__init__()
        self.request_id = request_id
    
    def filter(self, record):
        record.request_id = self.request_id
        return True


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Add request_id to request state
        request.state.request_id = request_id
        
        # Add context filter to loggers
        context_filter = LoggingContextFilter(request_id)
        info_logger.addFilter(context_filter)
        error_logger.addFilter(context_filter)
        request_logger.addFilter(context_filter)
        
        # Log request
        await self._log_request(request, request_id)
        
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Add request_id to response headers
            response.headers["X-Request-ID"] = request_id
            
            # Log response
            process_time = time.time() - start_time
            await self._log_response(request, response, process_time, request_id)
            
            return response
            
        except Exception as e:
            # Log exception
            process_time = time.time() - start_time
            error_logger.error(
                f"Unhandled exception: {str(e)}",
                exc_info=True,
                extra={"request_id": request_id}
            )
            raise
    
    async def _log_request(self, request: Request, request_id: str) -> None:
        """Log request details"""
        
        headers = dict(request.headers)
        body = None
        
        # Try to read body if it exists
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
            except:
                body = "Could not parse request body"
        
        request_data = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "headers": headers,
            "body": body,
            "client": request.client.host if request.client else None,
        }
        
        request_logger.info(
            f"Request: {json.dumps(request_data)}",
            extra={"request_id": request_id}
        )
    
    async def _log_response(
        self, request: Request, response: Response, process_time: float, request_id: str
    ) -> None:
        """Log response details"""
        
        response_data = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2),
            "headers": dict(response.headers),
        }
        
        request_logger.info(
            f"Response: {json.dumps(response_data)}",
            extra={"request_id": request_id}
        )
        
        # Log to info logger as well
        info_logger.info(
            f"{request.method} {request.url.path} {response.status_code} {round(process_time * 1000, 2)}ms",
            extra={"request_id": request_id}
        )
