import os
import sqlite3
from contextlib import closing

basedir = os.path.abspath(os.path.dirname(__file__))


def execute_query(query, args=()):
    """Executes a given SQL query on the 'chinook.db' SQLite database and returns the result."""
    path_to_db = os.path.join(basedir, 'chinook.db')

    try:
        with sqlite3.connect(path_to_db) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, args)
                connection.commit()
                records = cursor.fetchall()
    except (sqlite3.DatabaseError, sqlite3.IntegrityError, sqlite3.OperationalError) as e:
        print(f"Database error: {e}")
        records = []

    return records
