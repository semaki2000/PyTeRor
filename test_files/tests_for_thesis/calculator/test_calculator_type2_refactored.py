import pytest
from Calculator import Calculator


@pytest.mark.parametrize(
    "parametrized_var_0, parametrized_var_1, parametrized_var_2, parametrized_var_3, parametrized_var_4",
    [
        pytest.param(4, "deg", 2, 3, 6, id="test_multiplication_simple"),
        pytest.param(7, "rad", 0.3145, 4.2535, 1.3377258, id="test_multiplication_advanced"),
    ],
)
def test_multiplication_simple_parametrized(
    parametrized_var_0,
    parametrized_var_1,
    parametrized_var_2,
    parametrized_var_3,
    parametrized_var_4,
):
    calculator = Calculator(precision=parametrized_var_0, angle_unit=parametrized_var_1)
    (a, b) = (parametrized_var_2, parametrized_var_3)
    expected_result = parametrized_var_4
    actual_result = calculator.multiply(a, b)
    assert actual_result == expected_result



