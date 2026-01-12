"""
SQL recognition and generation content
"""
import os
import sqlite3
from Utils import global_var
from Core.add_item_sql import _db_path


def generate_from_sql():
    """
    Read database content and generate:
    1. items_list = [[item_name, expired_day, bar_name], ...]
    2. bar_name_list = [bar_name1, bar_name2, ...]  (skip NULL, remove duplicates)
    """
    print("reach here")

    # DB file under Utils directory
    db_path = _db_path()

    # Connect database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all items
    query = """
        SELECT item_name, expired_day, bar_name
        FROM items
        ORDER BY bar_name
    """
    cursor.execute(query)

    rows = cursor.fetchall()

    # items_list
    items_list = []
    for item_name, expired_day, bar_name in rows:
        items_list.append([item_name, expired_day, bar_name])

    # bar_name_list
    bar_name_list = []
    for _, _, bar_name in rows:
        if bar_name is None:
            continue
        if bar_name not in bar_name_list:
            bar_name_list.append(bar_name)

    # If you need to store into global_var:
    global_var.items_from_sql = items_list
    global_var.bars_from_sql = bar_name_list

    conn.close()
    print(items_list, bar_name_list)

    return items_list, bar_name_list