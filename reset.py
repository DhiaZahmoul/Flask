import sqlite3
def get_db_connection():
    conn = sqlite3.connect('database.sqlite')  # Path to your DB file
    conn.row_factory = sqlite3.Row  # Optional: to get rows as dict-like objects
    return conn
def reset_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            gender TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


reset_users_table()
