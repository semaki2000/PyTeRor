import pytest
from Calculator import Calculator


def test_addition_c():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    
    a, b = 2, 3
    expected_result = 5
    actual_result = calculator.add(a, b)
    assert actual_result == expected_result


def test_subtraction_c():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'

    a, b = 5, -3 #different values + different operator in front of constant.
    expected = 2 #different name
    actual_result = calculator.add(a, b)
    assert actual_result == expected
