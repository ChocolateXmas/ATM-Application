from scripts.pincode.pincode import Pincode
from scripts.config.config import Config
import mysql.connector
from scripts.config.utils import password_hasher

# These are only TEST users
users = {
    "Avi Cohen": {"id_num": "123456789", "pin": "1234", "balance": 1000},
    "Yossi Cohen": {"id_num": "123123123", "pin": "6543", "balance": 500},
    "Yuri Levi": {"id_num": "112210120", "pin": "5852", "balance": 800},
    "Alex Beigel": {"id_num": "827364575", "pin": "0420", "balance": 690360},
}

# Connect to MySQL
config = Config()

with config.connect() as (conn, cursor): 
    for name, info in users.items():
        try:
            # Insert into users table
            cursor.execute("INSERT INTO users (id_number, fullname, balance) VALUES (%s, %s, %s)", (info["id_num"], name, info["balance"]))
            user_id = cursor.lastrowid
            # Hash the PIN
            hashed_pin = password_hasher.hash(info["pin"])
            # Insert hashed PIN
            cursor.execute("INSERT INTO pincodes (user_id, pin) VALUES (%s, %s)", (user_id, hashed_pin))
        # END 
        except mysql.connector.IntegrityError:
            print(f"Duplicate ID - {info["id_num"]}, Skipping ...")
        # END IntegrityError
        except Exception as e:
            print(f"Error inserting user {name}: {e}")
            # Optionally, you can rollback the transaction if needed
            # conn.rollback()
        # END Exception
    # END for
    conn.commit()
# END with config.connect()