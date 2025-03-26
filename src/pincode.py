class Pincode:
    def __init__(self, pin: str):
        self.__pin = None
        self.set_pin(pin)
    # END __init__
   
    """
    Sets the pincode for the instance.

    Args:
        newPin (str): A string representing the new pincode. 
                        It must be a 4-digit numeric string.
    """ 
    def set_pin(self, newPin: str) -> None:
        if len(newPin) == 4 and newPin.isdigit():
            self.__pin = newPin  # Correctly using the parameter newPin
        else:
            raise ValueError("Pincode must be a 4 digit number")
    # END setPin

    """
        Returns the hash of the pincode if it is set.
        Raises a ValueError if the pincode is not set.
    """
    def __hash__(self):
        if self.__pin is None:
            raise ValueError("Pincode is not set and cannot be hashed")
        return hash(self.__pin)
    # END __hash__
# END Pincode