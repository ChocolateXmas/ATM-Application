# import pytest
# from app.scripts.pincode.pincode import PINManager, InvalidPIN

# @pytest.fixture
# def pin_mgr(tmp_path, monkeypatch):
#     # point PINManager at a temp file instead of real secrets
#     pin_file = tmp_path / "pin.db"
#     return PINManager(pin_file=str(pin_file))

# def test_set_and_check_pin(pin_mgr):
#     pin_mgr.set_pin("1234")
#     assert pin_mgr.verify_pin("1234") is True

# def test_wrong_pin(pin_mgr):
#     pin_mgr.set_pin("0000")
#     with pytest.raises(InvalidPIN):
#         pin_mgr.verify_pin("9999")
