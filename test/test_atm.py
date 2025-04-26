import pytest
from app.scripts.atm.atm import ATM, AMOUNT_INSUFFICIENT_BALANCE, AMOUNT_MULT_NOT_VALID

@pytest.fixture
def atm():
    # start each test with fresh account at $100 balance
    return ATM(start_balance=100)

def test_deposit_positive(atm):
    atm.deposit(50)
    assert atm.balance == 150

def test_deposit_negative_raises(atm):
    with pytest.raises(AMOUNT_MULT_NOT_VALID):
        atm.deposit(-20)

def test_withdraw_success(atm):
    atm.withdraw(25)
    assert atm.balance == 75

def test_withdraw_overdraft(atm):
    with pytest.raises(AMOUNT_INSUFFICIENT_BALANCE):
        atm.withdraw(200)

def test_balance_inquiry(atm):
    assert atm.get_balance() == 100
