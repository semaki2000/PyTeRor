import pytest
"""Tests that have pytest param in their decorators"""



@pytest.mark.parametrize(
    "parametrized_var_0", [pytest.param(1, id="test_a1"), pytest.param(2, id="test_b1")]
)
def test_a1_parametrized(parametrized_var_0):
    return parametrized_var_0



@pytest.mark.parametrize(
    "parametrized_var_0", [pytest.param(True, id="test_a2"), pytest.param(False, id="test_b2")]
)
def test_a2_parametrized(parametrized_var_0):
    return parametrized_var_0
