import pytest


def test_roman_numeral_4():
    rnc = RomanNumeralConverter()
    assert rnc.to_roman_numeral(4) == "IV"

def test_roman_numeral_10():
    rnc = RomanNumeralConverter()
    assert rnc.to_roman_numeral(10) == "X"

def test_roman_numeral_54():
    rnc = RomanNumeralConverter()
    assert rnc.to_roman_numeral(54) == "LIV"

def test_roman_numeral_111():
    rnc = RomanNumeralConverter()
    assert rnc.to_roman_numeral(111) == "CXI"

def test_roman_numeral_bad_input():
    rnc = RomanNumeralConverter()
    assert rnc.to_roman_numeral("foo") == False


class RomanNumeralConverter:
    def to_roman_numeral(self):
        return ""