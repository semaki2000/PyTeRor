import pytest
@pytest.mark.parametrize(
    "parametrized_name_0, parametrized_name_1",
    [
        pytest.param(a, a, id="test_a"),
        pytest.param(b, b, id="test_b"),
        pytest.param(a, b, id="test_both"),
    ],
)
def test_a_parametrized(parametrized_name_0, parametrized_name_1):
    a = 1
    b = 2
    parametrized_name_0 + parametrized_name_1


