import pytest
from Calculator import Calculator


def test_multiplication_simple():
    calculator = Calculator(precision=4, angle_unit='deg')
    
    a, b = 2, 3
    expected_result = 6
    
    actual_result = calculator.multiply(a, b)
    assert actual_result == expected_result


def test_multiplication_advanced():
    calculator = Calculator(precision=7, angle_unit='rad')

    a, b = 0.3145, 4.2535 
    expected = 1.3377258  

    actual_result = calculator.multiply(a, b)
    assert actual_result == expected

