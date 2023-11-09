import pytest

@pytest.mark.parametrize('parametrized_constant_0', [pytest.param('A', id='test_a_simple'), pytest.param('B', id='test_b_simple', marks=pytest.mark.example_mark), pytest.param('A', id='test_a_twice'), pytest.param('B', id='test_b_twice', marks=[pytest.mark.example_mark, pytest.mark.mark2])])
def test_a_simple_parametrized(parametrized_constant_0):
    assert parametrized_constant_0