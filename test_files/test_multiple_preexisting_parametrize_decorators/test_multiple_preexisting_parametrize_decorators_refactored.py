import pytest
#two clones, each with two preexisting parametrized parameter names

@pytest.mark.parametrize(
    "parametrized_name_0, parametrized_name_1, parametrized_var_0",
    [
        pytest.param(1, 3, "A", id="test_A1"),
        pytest.param(1, 4, "A", id="test_A1"),
        pytest.param(2, 3, "A", id="test_A1"),
        pytest.param(2, 4, "A", id="test_A1"),
        pytest.param(3, [4, 5, 6, 7], "B", id="test_A2"),
        pytest.param("value1", "value2", "B", id="test_A2"),
    ],
)
def test_A1_parametrized(parametrized_name_0, parametrized_name_1, parametrized_var_0):
    if parametrized_name_0 != parametrized_name_1:
        assert parametrized_var_0





"""


arg1: n1 original arguments
arg2: n2 original arguments

arg1 * n2, so that arg1 repeats n2 times. E.g: [1, 2, 3, 1, 2, 3]
for each arg in arg2, arg * n1, so that each arg in repeated n1 times in a row: ["a", "a", "a", "b", "b", "b"]

This then creates a single parametrize decorator:
@pytest.mark.parametrize("arg1, arg2", [ 
    (1, "a"),
    (2, "a"),
    (3, "a"),
    (1, "b"),
    (2, "b"),
    (3, "b")
    ])


"""
