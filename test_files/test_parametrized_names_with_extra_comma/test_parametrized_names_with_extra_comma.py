import pytest

@pytest.mark.parametrize("a, b, ", [(1, 2)])
def test_func(a, b):
    return 1


@pytest.mark.parametrize("c, d", [(1, 2)])
def test_func(a, b):
    return 1