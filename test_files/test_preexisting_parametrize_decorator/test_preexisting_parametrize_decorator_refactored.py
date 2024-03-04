import pytest
#two clones, each with two preexisting parametrized parameter names

@pytest.mark.parametrize(
    "parametrized_name_0, parametrized_name_1, parametrized_constant_0",
    [
        pytest.param(1, 2, "A", id="test_A1"),
        pytest.param(4, 5, "A", id="test_A1"),
        pytest.param(3, [4, 5, 6, 7], "B", id="test_A2"),
        pytest.param("value1", "value2", "B", id="test_A2"),
    ],
)
def test_A1_parametrized(parametrized_name_0, parametrized_name_1, parametrized_constant_0):
    if parametrized_name_0 != parametrized_name_1:
        assert parametrized_constant_0





"""
A1 - parametrize decorator

A2 - parametrize decorator with keywords instead of positional parameters


Target - parametrize decorator with
starts with: parametrized"arg1", "arg2"

"""

