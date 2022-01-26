import pytest

from daca.daca import Something


def test_daca_creation():
    x = Something()
    assert x is not None