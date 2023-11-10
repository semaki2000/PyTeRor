import pytest

@pytest.mark.parametrize(
    "parametrized_constant_0",
    [pytest.param(2, id="test_a_simple"), pytest.param(1, id="test_b_simple")],
)
def test_a_simple_parametrized(parametrized_constant_0):
    return parametrized_constant_0 + parametrized_constant_0


