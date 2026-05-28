import sqlite3

def init_db():
    conn = get_db()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('mechanic.db')
    conn.row_factory = sqlite3.Row  # lets you access columns by name like row['name']
    return conn

