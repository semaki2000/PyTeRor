import pytest

@pytest.mark.parametrize('parametrized_constant_0', [('A',), ('B',)])
def test_a_parametrized(parametrized_constant_0):
    assert parametrized_constant_0