import os
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database
DATABASE_URL = f"sqlite:///{BASE_DIR}/app/database/trading_alerts.db"

# API settings
API_V1_STR = "/api/v1"
PROJECT_NAME = "Trading Alerts API"

# Logging
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_DIR = BASE_DIR / "app" / "logs" / datetime.now().strftime("%Y-%m-%d")

# Create log directories if they don't exist
os.makedirs(LOG_DIR / "info", exist_ok=True)
os.makedirs(LOG_DIR / "error", exist_ok=True)
os.makedirs(LOG_DIR / "request", exist_ok=True)
