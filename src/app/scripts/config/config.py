import mysql.connector
import os
from .utils import read_secret


class Config:
    def __init__(self):
        self.config = {
            "user": read_secret("mysql_user"),
            "password": read_secret("mysql_password"),
            "host": os.environ["DB_HOST"],
            "database": os.environ["DB_NAME"],
        }
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="atm_pool", pool_size=5, pool_reset_session=True, **self.config
        )

    # END __init__

    def get_connection(self):
        return self.pool.get_connection()

    # END get_config

    def connect(self):
        class DB_Connection:
            def __init__(self, pool):
                self.conn = pool.get_connection()
                self.cursor = self.conn.cursor(dictionary=True)

            # END __init__

            def __enter__(self):
                return self.conn, self.cursor

            # END __enter__

            """
            context manager for closing the connection and cursor
            - exc_type	The type of the exception (e.g. ValueError)
            - exc_val	The actual exception instance (e.g. ValueError("Oops"))
            - exc_tb	Traceback object (for stack trace info)
            """

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.conn.close()
                self.cursor.close()

            # END __exit__

        # END DB_Connection
        return DB_Connection(self.pool)

    # END connect


# END Config
