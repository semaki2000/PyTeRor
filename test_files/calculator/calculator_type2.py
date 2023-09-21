import pytest
from Calculator import Calculator


def test_addition():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    
    a, b = 2, 3
    expected_result = 5
    actual_result = calculator.add(a, b)
    assert actual_result == expected_result


def test_addition2():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'

    a, b = 4, 3 #different values
    expected = 7 #different name 
    actual_result = calculator.add(a, b)
    assert actual_result == expected
