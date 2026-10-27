import sqlite3

def _add_user_id(conn, table):
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]
    if "user_id" not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN user_id INTEGER DEFAULT 0")

def get_conn():
    conn = sqlite3.connect("studentos.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        salt TEXT,
        password_hash TEXT)""")
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
    _add_user_id(conn, "expenses")
    _add_user_id(conn, "tasks")
    conn.commit()
    return conn