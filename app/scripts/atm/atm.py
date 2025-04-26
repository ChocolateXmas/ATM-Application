from scripts.pincode.pincode import Pincode
from scripts.config.config import Config
from scripts.constants.constants import USER_NOT_LOGGED_IN, \
                                        AMOUNT_MULT_NOT_VALID, \
                                        AMOUNT_INSUFFICIENT_BALANCE,\
                                        FAILED_UPDATE_BALANCE, \
                                        FAILED_UPDATE_PIN, \
                                        SERVER_CONNECTION_ERROR 
from scripts.config.utils import password_hasher as passowrd_hasher
import datetime
import mysql.connector

class Atm:
    def __init__(self):
        self.__id = None # ID primary key None if user is not logged in
        self.__userName = None # User None if user is not logged in
        self.__id_num = None # ID number None if user is not logged in
        self.__pinCode = None # Pincode None if user is not logged in
        self.__balance = None # Balance None if user is not logged in
        self.__loggedIn = False # True if user is logged in, False otherwise

        self.__db_config = Config() # MySQL connection pool
    # END __init__

    def __set_none(self) -> None:
        self.__id = None
        self.__userName = None
        self.__id_num = None
        self.__pinCode = None
        self.__balance = None
        self.__loggedIn = False
    # END __set_none

    """
        Returns True if user is logged in.
        False otherwise.
    """
    def is_logged_in(self) -> bool: 
        return self.__loggedIn
    # END __is_logged_in

    # Raises a ValueError if the user is not logged in
    def __ensure_logged_in(self) -> None:
        if not self.is_logged_in():
            raise ValueError(USER_NOT_LOGGED_IN)
    # END ensure_logged_in

    """
        False if user already logged in.
        Returns True if the user exists and the pin is correct.
        False otherwise.
    """
    def login(self, user_id_num: str, pin: str) -> bool:
        if self.is_logged_in():
            return False
        # END if
        try: 
            # MySQl connection
            with self.__db_config.connect() as (conn, cursor):
                # Step 1: SELECT user by fullname (names should ideally be unique or you use ID/username/email)
                cursor.execute("""
                    SELECT users.id, users.id_number, users.fullname, users.balance, pincodes.pin
                    FROM users
                    JOIN pincodes ON users.id = pincodes.user_id
                    WHERE users.id_number = %s
                """, (user_id_num,))
                result = cursor.fetchone()  # Or handle duplicates with fetchall()
                # Step 2: Compare entered PIN with hashed one
                try:
                    if result and passowrd_hasher.verify(result["pin"], pin):
                        self.__id = result["id"]
                        self.__userName = result["fullname"]
                        self.__id_num = result["id_number"]
                        self.__pincode = result["pin"]
                        self.__balance = result["balance"]
                        self.__loggedIn = True
                        return True
                    # END if
                    else:
                        return False
                    # END else
                except passowrd_hasher.VerifyMismatchError:
                    return False
                # END except VerifyMismatchError
                except Exception as e:
                    return False
                # END except Exception
            # END config.connect()
        # END try
        except mysql.connector.Error as err: 
            return False
        # END except mysql.connector.Error
        except Exception as e: 
            return False
        # END except Exception
    # END login

    ### DEPREACTED! Moved to login (by ID) ###
    """
        False if user already logged in.
        Returns True if the user exists and the pin is correct.
        False otherwise.
    """
    def login_username(self, fullName: str, pin: str) -> bool:
        if self.is_logged_in():
            return False
        # END if
        try: 
            # MySQl connection
            with self.__db_config.connect() as (conn, cursor):
                # Step 1: SELECT user by fullname (names should ideally be unique or you use ID/username/email)
                cursor.execute("""
                    SELECT users.id, users.id_number, users.fullname, users.balance, pincodes.pin
                    FROM users
                    JOIN pincodes ON users.id = pincodes.user_id
                    WHERE users.fullname = %s
                """, (fullName,))
                result = cursor.fetchone()  # Or handle duplicates with fetchall()
                # Step 2: Compare entered PIN with hashed one
                try:
                    if result and passowrd_hasher.verify(result["pin"], pin):
                        self.__id = result["id"]
                        self.__userName = result["fullname"]
                        self.__id_num = result["id_number"]
                        self.__pincode = result["pin"]
                        self.__balance = result["balance"]
                        self.__loggedIn = True
                        return True
                    # END if
                    else:
                        return False
                    # END else
                except passowrd_hasher.VerifyMismatchError:
                    return False
                # END except VerifyMismatchError
                except Exception as e:
                    return False
                # END except Exception
            # END config.connect()
        # END try
        except mysql.connector.Error as err: 
            return False
        # END except mysql.connector.Error
        except Exception as e: 
            return False
        # END except Exception
    # END login_username

    # Sets user's account info to None and logs out the user
    """
        Raises a ValueError if the user is not logged in.
        Continues regularly if the user log out successful, and sets all info to None.
    """
    def logOut(self) -> None:
        if not self.is_logged_in():
            raise ValueError(USER_NOT_LOGGED_IN)
        self.__set_none()
    # END logOut

    # Amount to deposit or withdraw must be a multiple of 20, 50 or 100
    def is_valid_amount(self, amount: float) -> bool:
        return True if (amount > 0 and (amount % 20 == 0 or amount % 50 == 0 or amount % 100 == 0)) else False
    # END is_valid_amount

    """
        Raises a ValueError if the user is not logged in.
        Raises a ValueError if the amount is not a multiple of 20, 50 or 100.
        Adds the amount to the user's balance.
    """
    def deposit(self, amount: float) -> None:
        self.__ensure_logged_in()
        if self.is_valid_amount(amount):
            self.__balance += amount
            self.__update_balance()
        else:
            raise ValueError(AMOUNT_MULT_NOT_VALID)
    # END deposit

    """
        Raises a ValueError if the user is not logged in.
        Raises a ValueError if the amount is not a multiple of 20, 50 or 100.
        Raises a ValueError if the amount is greater than the user's balance.
        Withdraws the amount from the user's balance.
    """
    def withdraw(self, amount: float) -> None:
        self.__ensure_logged_in()
        if amount > self.__balance:
            raise ValueError(AMOUNT_INSUFFICIENT_BALANCE)
        elif not self.is_valid_amount(amount):
            raise ValueError(AMOUNT_MULT_NOT_VALID)
        self.__balance -= amount
        self.__update_balance()
    # END withdraw
    
    # TODO: convert __update_balance to a function that updates the balance in the database
    def __update_balance(self) -> None:
        self.__ensure_logged_in()
        # users[self.__userName]["balance"] = self.__balance
        try:
            with self.__db_config.connect() as (conn, cursor):
                cursor.execute("""
                    UPDATE users
                    SET balance = %s
                    WHERE id_number = %s AND id = %s 
                """, (self.__balance, self.__id_num, self.__id))
                conn.commit()
            # END with config.connect()
        except mysql.connector.Error as err:
            raise ValueError(SERVER_CONNECTION_ERROR)
        except Exception as e:
            raise ValueError(FAILED_UPDATE_BALANCE)
    # END __update_balance

    """
        Returns the user's full name.
        Returns None if the user is not logged in.
    """
    def get_user_name(self) -> str: return self.__userName
    
    def set_user_name(self, fullName: str) -> str: self.__userName = fullName

    def get_balance(self) -> float: return self.__balance

    # TODO: convert __get_pin to a function that changes the pin in the database
    def change_pin(self, newPin: str) -> None:
        self.__ensure_logged_in()
        try:
            with self.__db_config.connect() as (conn, cursor): 
                cursor.execute("""
                    UPDATE pincodes
                    SET pin = %s
                    WHERE user_id = %s
                """, (passowrd_hasher.hash(newPin), self.__id))
                conn.commit()
            # END with db_config.connect
        except mysql.connector.Error as err:
            raise ValueError(SERVER_CONNECTION_ERROR)
        except Exception as e:
            raise ValueError(FAILED_UPDATE_PIN)
    # END change_pin

    def get_recipe(self) -> list:
        self.__ensure_logged_in()
        now = datetime.datetime.now() # get the current date and time
        current_date = now.strftime("%d/%m/%y %H:%M:%S") # format the date and time
        return [
            f"Hello {self.__userName},",
            f"At this moment DATE: {current_date} you got {self.__balance} NIS in your account",
            f"Thank you for using our ATM service"
        ]
    # END get_recipe
# END Atm