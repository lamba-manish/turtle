# Trading Alerts API

A FastAPI-based API for trading alerts with ICICI Breeze integration.

## Setup

1. Install dependencies:
```bash
uv pip install fastapi uvicorn sqlalchemy alembic aiosqlite pydantic python-dotenv
```

2. Run database migrations:
```bash
alembic upgrade head
```

3. Run the application:
```bash
python3 -m app.main
```

## API Documentation

API documentation is available at `/docs` when the server is running.

## Project Structure

```
/app/
  ├── config.py           # Configuration variables
  ├── main.py             # FastAPI application
  ├── database/           # Database models and connection
  ├── routers/            # API endpoints
  ├── schemas/            # Pydantic models
  ├── services/           # Business logic
  ├── middleware/         # Middleware components
  └── logs/{YYYY-MM-DD}/  # Log files
      ├── info/           # General operation logs
      ├── error/          # Error logs
      └── request/        # Request/response logs
```

## Features

- Health check endpoint at `/api/v1/health`
- Database health check endpoint at `/api/v1/db-health`
- Request ID tracking
- Comprehensive logging system
- SQLite database with SQLAlchemy ORM
