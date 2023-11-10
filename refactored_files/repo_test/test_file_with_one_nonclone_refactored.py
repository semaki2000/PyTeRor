import pytest

@pytest.mark.parametrize('parametrized_constant_0', [pytest.param('A', id='test_a'), pytest.param('B', id='test_b')])
def test_a_parametrized(parametrized_constant_0):
    assert parametrized_constant_0

def test_c_non_clone():
    return 1 + 1