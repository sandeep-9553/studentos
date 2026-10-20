import sqlite3

def get_conn():
    conn = sqlite3.connect("studentos.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        amount REAL,
        category TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        subject TEXT,
        deadline TEXT,
        priority TEXT,
        hours_needed REAL,
        done INTEGER DEFAULT 0)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS profile(
        id INTEGER PRIMARY KEY,
        target_role TEXT,
        skills TEXT)""")
    conn.commit()
    return conn