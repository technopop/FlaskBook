import pytest


@pytest.fixture
def app_data():
    return 3


def test_func1():
    assert 1 == 1


def test_func2():
    assert 2 == 2
