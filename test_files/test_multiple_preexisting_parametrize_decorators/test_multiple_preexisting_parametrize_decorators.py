import pytest
#two clones, each with two preexisting parametrized parameter names

@pytest.mark.parametrize("arg1", [1, 2])
@pytest.mark.parametrize("arg2", [3, 4])
def test_A1(arg1, arg2):
    if arg1 != arg2:
        assert """A"""



@pytest.mark.parametrize("arg3, arg4", [(3, [4,5,6,7]), ("value1", "value2")])
def test_A2(arg3, arg4):
    if arg3 != arg4:
        assert "B"


"""


arg1: n1 original arguments
arg2: n2 original arguments

arg1 * n2, so that arg1 repeats n2 times. E.g: [1, 2, 3, 1, 2, 3]
for each arg in arg2, arg * n1, so that each arg in repeated n1 times in a row: ["a", "a", "a", "b", "b", "b"]

This then creates a single parametrize decorator:
@pytest.mark.parametrize("arg1, arg2", [ 
    (1, "a"),
    (2, "a"),
    (3, "a"),
    (1, "b"),
    (2, "b"),
    (3, "b")
    ])


"""
