import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               fullname TEXT NOT NULL,
               balance INTEGER NOT NULL,
               )
               """)

cursor.commit()
cursor.close()