import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'mechanic.db'))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open(os.path.join(BASE_DIR, 'schema.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()