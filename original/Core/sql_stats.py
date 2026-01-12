"""
SQL data statistics code
"""
import sqlite3
import os
from datetime import datetime, date
from Core.add_item_sql import _db_path


def get_sql_stats():
    """
    Return SQL statistical information, including:
    - Quantity of each category
    - Item name list corresponding to each category
    """

    conn = sqlite3.connect(_db_path())
    cur = conn.cursor()

    cur.execute("""
        SELECT item_name, expired_day
        FROM items
    """)

    rows = cur.fetchall()
    conn.close()

    # Four category structure
    stats = {
        ">30": [],
        "7~30": [],
        "<7": [],
        "expired": []
    }

    today = date.today()

    for item_name, expired_day in rows:
        try:
            d = datetime.strptime(expired_day, "%Y-%m-%d").date()
            diff = (d - today).days
        except:
            continue

        if diff > 30:
            stats[">30"].append(item_name)
        elif 7 <= diff <= 30:
            stats["7~30"].append(item_name)
        elif 0 <= diff < 7:
            stats["<7"].append(item_name)
        else:
            stats["expired"].append(item_name)

    return stats