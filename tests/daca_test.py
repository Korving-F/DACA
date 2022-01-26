import pytest

from daca.daca import Test

def test_daca_creation():
    x = Test()
    assert x is not None