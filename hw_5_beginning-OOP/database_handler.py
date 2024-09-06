import os

import sqlite3

basedir = os.path.abspath(os.path.dirname(__file__))


def execute_query(query, args=()):
    path_to_db = os.path.join(basedir, 'chinook.db')
    with sqlite3.connect(path_to_db) as connection:
        cursor = connection.cursor()
        cursor.execute(query, args)
        connection.commit()

        records = cursor.fetchall()

    return records
