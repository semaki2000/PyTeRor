import pytest
#two clones, each with two preexisting parametrized parameter names

@pytest.mark.parametrize("arg1, arg2", [(1, 2), (4, 5)])
def test_A1(arg1, arg2):
    if arg1 != arg2:
        assert """A"""



@pytest.mark.parametrize(argnames="arg3, arg4", argvalues=[(3, [4,5,6,7]), ("value1", "value2")])
def test_A2(arg3, arg4):
    if arg3 != arg4:
        assert "B"


"""
A1 - parametrize decorator

A2 - parametrize decorator with keywords instead of positional parameters


Target - parametrize decorator with
starts with: parametrized"arg1", "arg2"

"""

