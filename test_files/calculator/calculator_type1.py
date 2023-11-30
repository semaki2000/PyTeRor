import pytest
from Calculator import Calculator


def test_addition_type1():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    
    a, b = 2, 3
    expected_result = 5
    actual_result = calculator.add(a, b)
    assert actual_result == expected_result

def test_addition2_type1():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    
    a, b = 2, 3
    expected_result = 5
    actual_result = calculator.add(a, b)
    assert actual_result == expected_result

"""Nothing should happen here.
Type 1 clone."""