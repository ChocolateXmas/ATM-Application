import mysql.connector
import os
from dotenv import load_dotenv

# Try to load environment variables, but don't fail if file doesn't exist
try:
    load_dotenv(".env.development")
except Exception as e:
    print(f"Warning: Could not load .env.development file: {e}")

# Set default values for Docker environment
config = {
    'host': os.getenv("DB_HOST", "mysql"),
    'user': os.getenv("DB_USER", "atm_user"),
    'password': None,
    'database': os.getenv("DB_NAME", "atm_db")
}

# Read password from Docker secret
try:
    with open("/run/secrets/db_user_password", "r") as f:
        config['password'] = f.read().strip()
except Exception as e:
    print(f"Error reading password file: {e}")
    exit(1)

def init_db():
    try:
        with mysql.connector.connect(**config) as conn:
            with conn.cursor() as cursor:
                with open("Database/schema.sql", "r") as f:
                    sql_commands = f.read()
                    for statement in sql_commands.strip().split(";"):
                        if statement.strip():
                            cursor.execute(statement)
                conn.commit()
                print("[✓] Database initialized from schema.sql.")
    # END try
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
# END init_db

if __name__ == "__main__":
    init_db()
