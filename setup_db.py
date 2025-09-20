import os
import sys
import sqlite3

# Create the database directory if it doesn't exist
os.makedirs('app/database', exist_ok=True)

# Create an empty SQLite database file
conn = sqlite3.connect('app/database/trading_alerts.db')
conn.close()

print("Database file created successfully.")
