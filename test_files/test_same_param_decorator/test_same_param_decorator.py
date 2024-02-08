import pytest
#two clones with the same parametrize decorators

@pytest.mark.parametrize("arg1, arg2", [(1, 2), (4, 5)])
def test_A1(arg1, arg2):
    if arg1 != arg2:
        assert """A"""



@pytest.mark.parametrize("arg1, arg2", [(1, 2), (4, 5)])
def test_A2(arg1, arg2):
    if arg1 != arg2:
        assert "B"


"""
A1 - parametrize decorator with
arg1: 1, '1'
arg2: 2, '2'

A2 - parametrize decorator with
arg1: 3, '3'
arg2: 4, '4'


Target - parametrize decorator with
starts with: parametrized"arg1", "arg2"
"""
