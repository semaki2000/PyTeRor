import pytest
from Calculator import Calculator


@pytest.mark.parametrize(
    "parametrized_constant_0, parametrized_constant_1, parametrized_constant_2, parametrized_constant_3, parametrized_constant_4",
    [
        pytest.param(4, "deg", 2, 3, 6, id="test_multiplication_simple"),
        pytest.param(7, "rad", 0.3145, 4.2535, 1.3377258, id="test_multiplication_advanced"),
    ],
)
def test_multiplication_simple_parametrized(
    parametrized_constant_0,
    parametrized_constant_1,
    parametrized_constant_2,
    parametrized_constant_3,
    parametrized_constant_4,
):
    calculator = Calculator(precision=parametrized_constant_0, angle_unit=parametrized_constant_1)
    (a, b) = (parametrized_constant_2, parametrized_constant_3)
    expected_result = parametrized_constant_4
    actual_result = calculator.multiply(a, b)
    assert actual_result == expected_result




@pytest.mark.parametrize(
    "parametrized_constant_0, parametrized_constant_1, parametrized_constant_2, parametrized_constant_3, parametrized_constant_4",
    [
        pytest.param(4, "deg", 2, 3, 6, id="test_subtraction_simple"),
        pytest.param(7, "rad", 0.3145, 4.2535, 1.3377258, id="test_subtraction_advanced"),
    ],
)
def test_subtraction_simple_parametrized(
    parametrized_constant_0,
    parametrized_constant_1,
    parametrized_constant_2,
    parametrized_constant_3,
    parametrized_constant_4,
):
    calculator = Calculator(precision=parametrized_constant_0, angle_unit=parametrized_constant_1)
    (a, b) = (parametrized_constant_2, parametrized_constant_3)
    expected_result = parametrized_constant_4
    actual_result = calculator.subtract(a, b)
    assert actual_result == expected_result




@pytest.mark.parametrize(
    "parametrized_constant_0, parametrized_constant_1, parametrized_constant_2, parametrized_constant_3, parametrized_constant_4",
    [
        pytest.param(4, "deg", 2, 3, 6, id="test_addition_simple"),
        pytest.param(7, "rad", 0.3145, 4.2535, 1.3377258, id="test_addition_advanced"),
    ],
)
def test_addition_simple_parametrized(
    parametrized_constant_0,
    parametrized_constant_1,
    parametrized_constant_2,
    parametrized_constant_3,
    parametrized_constant_4,
):
    calculator = Calculator(precision=parametrized_constant_0, angle_unit=parametrized_constant_1)
    (a, b) = (parametrized_constant_2, parametrized_constant_3)
    expected_result = parametrized_constant_4
    actual_result = calculator.add(a, b)
    assert actual_result == expected_result



