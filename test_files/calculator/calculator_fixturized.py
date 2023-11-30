import pytest
from Calculator import Calculator

@pytest.fixture
def calculator():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'
    return calculator

def test_addition_f(calculator):
    a, b = 1, 2
    expected_result = 3

    actual_result = calculator.add(a, b)
    assert actual_result == expected_result

def test_addition2_f(calculator):
    a, b = 4, 5
    expected_result = 6

    actual_result = calculator.add(a, b)
    assert actual_result == expected_result

"""Fixture should remain. The others should be refactored"""