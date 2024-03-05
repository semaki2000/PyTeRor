import pytest

@pytest.fixture
def f():
    return 1

@pytest.mark.parametrize(
    "parametrized_name_0",
    [
        pytest.param(1, id="test_a"),
        pytest.param(2, id="test_a"),
        pytest.param(3, id="test_b"),
        pytest.param(4, id="test_b"),
        pytest.param(f, id="test_f"),
    ],
)
def test_a_parametrized(parametrized_name_0):
    assert parametrized_name_0


