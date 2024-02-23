"""
Test that any unknown decorators are kept in their original position, as otherwise it could affect functionality.
"""


import pytest
#two clones with the same parametrize decorators

@func_a
@func_b
@pytest.mark.parametrize("arg1, arg2", [(1, 2), (4, 5)])
@pytest.mark.a
def test_A1(arg1, arg2):
    if arg1 != arg2:
        assert """A"""


@func_a
@func_b
@pytest.mark.parametrize("arg1, arg2", [(1, 2), (4, 5)])
@pytest.mark.a
def test_A2(arg1, arg2):
    if arg1 != arg2:
        assert "B"


