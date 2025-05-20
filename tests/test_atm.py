import pytest
from unittest.mock import patch
from src.app.scripts.atm.atm import Atm, \
                                AMOUNT_INSUFFICIENT_BALANCE, \
                                AMOUNT_MULT_NOT_VALID


@pytest.fixture
def atm():
    # Patch Config.__init__ before creating Atm instance, so db queries will not be execeuted
    with patch('src.app.scripts.config.config.Config.__init__', lambda self: setattr(self, 'pool', None)):
        atm = Atm()
        # Stub __update_balance to avoid DB access
        atm._Atm__update_balance = lambda: None
        atm._Atm__balance = 100
        atm._Atm__loggedIn = True
        return atm
# END atm

def test_deposit_positive(atm):
    # With __update_balance stubbed, deposit logic can be tested in isolation
    atm.deposit(50)
    assert atm.get_balance() == 150
# ENE test_deposit_positive

def test_deposit_negative_raises(atm):
    # Negative deposit should raise the AMOUNT_MULT_NOT_VALID error
    with pytest.raises(ValueError) as excinfo:
        atm.deposit(-20)
    assert str(excinfo.value) == AMOUNT_MULT_NOT_VALID
# test_deposit_negative_raises

def test_withdraw_success(atm):
    atm.withdraw(100)
    assert atm.get_balance() == 0
# END test_withdraw_success

def test_withdraw_invalid_mult(atm):
    with pytest.raises(ValueError) as execinfo:
        atm.withdraw(25)
    assert str(execinfo.value) == AMOUNT_MULT_NOT_VALID
    with pytest.raises(ValueError) as execinfo:
        atm.withdraw(37)
    assert str(execinfo.value) == AMOUNT_MULT_NOT_VALID
# END test_withdraw_invalid_mult

def test_withdraw_overdraft(atm):
    with pytest.raises(ValueError) as excinfo:
        atm.withdraw(200)
    assert str(excinfo.value) == AMOUNT_INSUFFICIENT_BALANCE
# END test_withdraw_overdraft

def test_balance_inquiry(atm):
    assert atm.get_balance() == 100
# END test_balance_inquiry