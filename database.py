import sqlite3
import os

DB_NAME = "symposium.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            college_name TEXT NOT NULL,
            dept_year TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT NOT NULL,
            events TEXT NOT NULL,
            accommodation TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_user(data):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (full_name, college_name, dept_year, mobile, email, events, accommodation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['full_name'],
            data['college_name'],
            data['dept_year'],
            data['mobile'],
            data['email'],
            data['events'],
            data['accommodation']
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY timestamp DESC').fetchall()
    conn.close()
    return users

def get_stats():
    conn = get_db_connection()
    total = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    accommodation_count = conn.execute('SELECT COUNT(*) FROM users WHERE accommodation = "Yes"').fetchone()[0]
    conn.close()
    return {
        "total": total,
        "accommodation": accommodation_count
    }

# Initialize the DB immediately when imported (safe for simple script)
if not os.path.exists(DB_NAME):
    init_db()
else:
    # Ensure table exists even if file exists
    init_db()
