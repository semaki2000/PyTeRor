import pytest
#two clones, where one has a mark

def test_a():
    assert """A"""

def test_b():
    assert "B"

def test_c_non_clone():
    return 1+1