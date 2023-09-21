import pytest
from Calculator import Calculator


@pytest.mark.parametrize('angle_unit', ["deg", "rad", "grad"])
def test_addition(angle_unit):
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = angle_unit
    
    a, b = 2, 3
    expected_result = 5
    actual_result = calculator.add(a, b)
    assert actual_result == expected_result


def test_addition2():
    calculator = Calculator()
    calculator.precision = 4
    calculator.angle_unit = 'deg'

    a, b = 5, 3 #different values
    expected = 8 #different name 
    actual_result = calculator.add(a, b)
    assert actual_result == expected
