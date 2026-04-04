import sqlite3
from datetime import datetime
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Connect to the database
conn = sqlite3.connect('data/tracker.db')
cursor = conn.cursor()

def setup_database():
    """Creates the necessary tables if they are missing."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            app_id TEXT PRIMARY KEY,
            name TEXT,
            target_price REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_id TEXT,
            price REAL,
            date_checked TEXT,
            FOREIGN KEY (app_id) REFERENCES games (app_id)
        )
    ''')
    conn.commit()

def add_game(app_id, name, target_price):
    """Adds a game to track."""
    cursor.execute('''
        INSERT INTO games (app_id, name, target_price)
        VALUES (?, ?, ?)
        ON CONFLICT(app_id) DO UPDATE SET
            name=excluded.name,
            target_price=excluded.target_price
    ''', (app_id, name, target_price))
    conn.commit()

def log_price(app_id, price):
    """Saves today's price."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''
        SELECT id FROM price_history 
        WHERE app_id = ? AND date_checked = ?
    ''', (app_id, today))
    
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO price_history (app_id, price, date_checked)
            VALUES (?, ?, ?)
        ''', (app_id, price, today))
        conn.commit()
        print(f"[DB] Logged ${price} for App {app_id} on {today}")
    else:
        print(f"[DB] Price for App {app_id} already logged today.")

if __name__ == "__main__":
    setup_database()
    print("Database initialized.")