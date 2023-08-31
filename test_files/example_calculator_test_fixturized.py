import pytest
from Calculator import Calculator

@pytest.fixture
def calculator():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    return calculator

def test_addition(calculator):
    a, b = 2, 3
    expected_result = 5

    actual_result = calculator.add(a, b)
    assert actual_result == expected_result

def test_subtraction(calculator):
    a, b = 5, 3
    expected_result = 2

    actual_result = calculator.subtract(a, b)
    assert actual_result == expected_result
