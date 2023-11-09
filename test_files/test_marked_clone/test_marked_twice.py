import pytest
#two clones, where one has a mark

def test_a_twice():
    assert "A"

@pytest.mark.example_mark
@pytest.mark.mark2
def test_b_twice():
    assert "B"


#should become for the refactored version
#@pytest.mark.parametrize("new_var", [
#    pytest.param("A", id="test_a"),
#    pytest.param("B", marks=[pytest.mark.example_mark, pytest.mark.mark2], id="test_b"),
#])
#def test_a_parametrized(new_var):
#    assert new_var