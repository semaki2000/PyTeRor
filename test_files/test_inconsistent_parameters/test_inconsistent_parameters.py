import pytest

@pytest.fixture
def f():
    return 1

@pytest.mark.parametrize("a", [1, 2])
def test_a(a):
    assert a

@pytest.mark.parametrize("b", [3, 4])
def test_b(b):
    assert b

def test_f(f):
    assert f
