"""
SQL main logic code, including add/modify/delete database operations
"""
import sqlite3
import os
from Utils.global_var import ensure_writable_db


def _db_path():
    """
    Get writable database path (persisted in %APPDATA%)
    """
    return ensure_writable_db()
DB_PATH = _db_path()


def setup_database():
    """
    Initialize database (only items table required)
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            expired_day TEXT,
            bar_name TEXT DEFAULT NULL
        )
    """)

    conn.commit()
    conn.close()


def insert_products(item_name, expired_day):
    """
    Insert new item into SQL
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO items(item_name, expired_day, bar_name)
        VALUES (?, ?, NULL)
    """, (item_name, expired_day))

    conn.commit()
    conn.close()


def update_item_bar_name(item_name, bar_name):
    """
    Update item's bar_name (when attached or moved back to left side)
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE items
        SET bar_name = ?
        WHERE item_name = ?
    """, (bar_name, item_name))

    conn.commit()
    conn.close()


def delete_item(item_name):
    """
    Delete a single item (used when dumping into trash bin)
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM items WHERE item_name = ?", (item_name,))

    conn.commit()
    conn.close()


def load_all_items():
    """
    Load all items
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT item_id, item_name, expired_day, bar_name
        FROM items
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "item_id": r[0],
            "item_name": r[1],
            "expired_day": r[2],
            "bar_name": r[3]
        }
        for r in rows
    ]


def clear_all_items():
    """
    Clear entire table (Menu → Clear Database)
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM items")

    conn.commit()
    conn.close()