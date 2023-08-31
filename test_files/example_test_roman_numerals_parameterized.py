import pytest



@pytest.mark.parametrize(
    "test_input, expected",
    [
        (4, "IV"), 
        (10, "X"), 
        (54, "LIV"),
        (111, "CXI"),
        ("foo", False) #bad input
    ]
)
def test_roman_numeral(test_input, expected):
    rnc = RomanNumeralConverter()
    assert rnc.to_roman_numeral(test_input) == expected



class RomanNumeralConverter:
    def to_roman_numeral(self):
        return ""