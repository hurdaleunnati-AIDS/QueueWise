
import sqlite3
from pathlib import Path


# Find the main QueueWise project folder
BASE_FOLDER = Path(__file__).resolve().parent.parent

# Database file location
DATABASE_PATH = BASE_FOLDER / "queuewise.db"


def create_table():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            observed_at TEXT NOT NULL UNIQUE,
            entries INTEGER NOT NULL,
            exits INTEGER NOT NULL,
            occupancy INTEGER NOT NULL,
            source TEXT NOT NULL,
            data_mode TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def insert_reading(observed_at, entries, exits, occupancy, source, data_mode):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO readings
        (observed_at, entries, exits, occupancy, source, data_mode)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (observed_at, entries, exits, occupancy, source, data_mode))

    connection.commit()

    inserted = cursor.rowcount == 1

    connection.close()

    return inserted


def get_readings():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT observed_at, entries, exits, occupancy, source, data_mode
        FROM readings
        ORDER BY observed_at ASC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_reading_count():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM readings")

    count = cursor.fetchone()[0]

    connection.close()

    return count
