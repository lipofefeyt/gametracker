import sqlite3
from datetime import datetime
import os

_conn = None

def _get_conn():
    global _conn
    if _conn is None:
        os.makedirs('data', exist_ok=True)
        _conn = sqlite3.connect('data/tracker.db')
    return _conn

def setup_database():
    """Creates the necessary tables if they are missing."""
    conn = _get_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS games (
            app_id TEXT PRIMARY KEY,
            name TEXT,
            target_price REAL,
            store TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_id TEXT,
            price REAL,
            date_checked TEXT,
            FOREIGN KEY (app_id) REFERENCES games (app_id)
        )
    ''')
    conn.commit()

def add_game(app_id, name, target_price, store):
    """Adds a game to track."""
    conn = _get_conn()
    conn.execute('''
        INSERT INTO games (app_id, name, target_price, store)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(app_id) DO UPDATE SET
            name=excluded.name,
            target_price=excluded.target_price,
            store=excluded.store
    ''', (app_id, name, target_price, store))
    conn.commit()

def get_games():
    """Returns all tracked games as a list of (app_id, name, target_price, store) tuples."""
    conn = _get_conn()
    cursor = conn.execute("SELECT app_id, name, target_price, store FROM games")
    return cursor.fetchall()

def log_price(app_id, price):
    """Saves today's price if not already logged."""
    conn = _get_conn()
    today = datetime.now().strftime("%Y-%m-%d")

    cursor = conn.execute(
        "SELECT id FROM price_history WHERE app_id = ? AND date_checked = ?",
        (app_id, today)
    )
    if not cursor.fetchone():
        conn.execute(
            "INSERT INTO price_history (app_id, price, date_checked) VALUES (?, ?, ?)",
            (app_id, price, today)
        )
        conn.commit()
        print(f"[DB] Logged €{price} for App {app_id} on {today}")
    else:
        print(f"[DB] Price for App {app_id} already logged today.")

if __name__ == "__main__":
    setup_database()
    print("Database initialized.")
