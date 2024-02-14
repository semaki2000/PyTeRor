import pytest

"""
Two clones, where one has a pre-existing parametrize decorator, and another does not.
Expected behaviour:

A parametrized test with decorator:
@pytest.mark.parametrize("parametrized_name_0, parametrized_name_1", [(1, 2), (4, 5), (outer_1, outer_2)])

"""

outer_1, outer_2 = "a"


@pytest.mark.parametrize("arg1, arg2", [(1, 2), (4, 5)])
def test_A1(arg1, arg2):
    if arg1 != arg2:
        assert """A"""


def test_A2(outer_1, outer_2):
    if outer_1 != outer_2:
        assert "A"


