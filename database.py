import sqlite3
import time
from pathlib import Path


DB_PATH = Path(__file__).parent / "data.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS raw_data (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                received_at INTEGER NOT NULL,
                data        BLOB    NOT NULL
            );
        """)


def insert_data(data: bytes) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO raw_data (received_at, data) VALUES (?, ?)",
            (int(time.time()), data),
        )
