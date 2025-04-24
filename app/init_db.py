import mysql.connector
import os
from scripts.config.config import Config

script_name = os.path.basename(__file__) # get the current script file name

def init_db():
    config = Config()
    try:
        with config.connect() as (conn, cursor):
            with open("database/schema.sql", "r") as f:
                sql_commands = f.read()
                for statement in sql_commands.strip().split(";"):
                    if statement.strip():
                        cursor.execute(statement)
            # END with open
            conn.commit()
            print(f"{script_name} | [✓] Database initialized from schema.sql.")
        # END with config.connect()
    # END try   
    except mysql.connector.Error as err:
        print(f"{script_name} | Error initializing database: {err}")
        exit(1)
    # END mysql.connector.Error
    except Exception as e:
        print(f"{script_name} | Unexpected error: {e}")
        exit(1)
    # END Exception
# END init_db

if __name__ == "__main__":
    init_db()
