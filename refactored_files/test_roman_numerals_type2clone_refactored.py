import pytest

@pytest.mark.parametrize('new_var_0, new_var_1', [(4, 'IV'), (10, 54), (111, 'foo'), ('X', 'LIV'), ('CXI', False)])
def test_roman_numeral_4(new_var_0, new_var_1):
    rnc = RomanNumeralConverter()
    assert rnc.to_roman_numeral(new_var_0) == new_var_1

class RomanNumeralConverter:

    def to_roman_numeral(self, thing):
        return ''