import pytest
from app.models.user import User


def test_password_setter():
    u = User(password='cat')
    assert u.password_hash != None


def test_no_password_getter():
    u = User(password='cat')
    with pytest.raises(AttributeError):
        u.password


def test_password_verification():
    u = User(password='cat')
    assert u.verify_password('cat') == True
    assert u.verify_password('dog') == False


def test_password_salts_are_random():
    u1 = User(password='cat')
    u2 = User(password='cat')
    assert u1.password_hash != u2.password_hash