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
Running on these two tests should give an output file with one test, two parametrize decorators.
Pre-existing parametrize decorator is kept.
However, if they had not been equal, a single parametrize decorator would be created.
"""
