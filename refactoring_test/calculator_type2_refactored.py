import pytest
from Calculator import Calculator

@pytest.mark.parametrize('var1, var2', [(1, 2), (2, 3), (3, 4)])
def test_addition():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    (a, b) = (2, 3)
    expected_result = 5
    actual_result = calculator.add(a, b)
    assert actual_result == expected_result

def test_subtraction():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    (a, b) = (5, 3)
    expected_result = 2
    actual_result = calculator.subtract(a, b)
    assert actual_result == expected_result