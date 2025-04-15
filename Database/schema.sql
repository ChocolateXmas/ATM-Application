-- import sqlite3

-- conn = sqlite3.connect("users.db")

-- cursor = conn.cursor()

-- cursor.execute("""
--     CREATE TABLE IF NOT EXISTS users(
--                id INTEGER PRIMARY KEY AUTOINCREMENT,
--                fullname TEXT NOT NULL,
--                balance INTEGER NOT NULL,
--                )
--                """)

-- cursor.commit()
-- cursor.close()

CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    balance INT NOT NULL
);