import pytest
from Calculator import Calculator

@pytest.mark.parametrize('new_var_0, new_var_1', [(2, 5), (4, 7)])
def test_addition(new_var_0, new_var_1):
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    (a, b) = (new_var_0, 3)
    expected_result = new_var_1
    actual_result = calculator.add(a, b)
    assert actual_result == expected_result