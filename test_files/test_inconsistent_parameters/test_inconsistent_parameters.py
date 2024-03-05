import pytest

@pytest.fixture
def f():
    pass

@pytest.mark.parametrize("a", [1, 2])
def test_a(a):
    return a

@pytest.mark.parametrize("b", [3, 4])
def test_b(b):
    return b

def test_f(f):
    return f
