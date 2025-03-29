from pincode import Pincode

users = {
    "Avi Cohen": {"pin": Pincode("1234"), "balance": 1000},
    "Yossi Cohen": {"pin": Pincode("6543"), "balance": 500},
    "Yuri Levi": {"pin": Pincode("5852"), "balance": 800},
}

class Atm:
    def __init__(self):
        self.__userName = None # User None if user is not logged in
        self.__pinCode = None # Pincode None if user is not logged in
        self.__balance = None # Balance None if user is not logged in
        self.__loggedIn = False # True if user is logged in, False otherwise
    # END __init__

    """
        Returns True if user is logged in.
        False otherwise.
    """
    def __is_logged_in(self) -> bool: 
        return self.__loggedIn
    # END __is_logged_in

    """
        False if user already logged in.
        Returns True if the user exists and the pin is correct.
        False otherwise.
    """
    def login(self, fullName: str, pin: str) -> bool:
        if self.__is_logged_in():
            return False
        if fullName in users:
            if hash(users[fullName]["pin"]) == hash(pin):
                self.__userName = fullName
                self.__pincode = hash(pin)
                self.__balance = users[fullName]["balance"]
                self.__loggedIn = True
                return True
        return False
    # END login

    # Sets user's account info to None and logs out the user
    """
        Raises a ValueError if the user is not logged in.
        Continues regularly if the user log out successful, and sets all info to None.
    """
    def logOut(self) -> None:
        if not self.__is_logged_in():
            raise ValueError("User is not logged in")
        self.__userName = None
        self.__pinCode = None
        self.__balance = None
        self.__loggedIn = False
    # END logOut

    # Amount to deposit or withdraw must be a multiple of 20, 50 or 100
    def is_valid_amount(self, amount: float) -> bool:
        return True if (amount > 0 and (amount % 20 == 0 or amount % 50 == 0 or amount % 100 == 0)) else False
    # END is_valid_amount

    # Raises a ValueError if the user is not logged in
    def __ensure_logged_in(self) -> None: 
        if not self.__is_logged_in():
            raise ValueError("User is not logged in")
    # END ensure_logged_in

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
            raise ValueError("Amount must be a multiple of 20, 50 or 100")
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
            raise ValueError("Insufficient NIS Balance")
        elif not self.is_valid_amount(amount):
            raise ValueError("Amount must be a multiple of 20, 50 or 100")
        self.__balance -= amount
        self.__update_balance()
    # END withdraw

    def __update_balance(self) -> None:
        users[self.__userName]["balance"] = self.__balance
    # END __update_balance

    def get_user_name(self) -> str: return self.__userName
    def set_user_name(self, fullName: str) -> str: self.__userName = fullName

    def get_balance(self) -> float: return self.__balance

    def quit(self):
        pass
    # END Atm
# END Atm