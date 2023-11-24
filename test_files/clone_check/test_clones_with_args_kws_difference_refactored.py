import pytest


@pytest.mark.parametrize(
    "parametrized_name_0", [pytest.param(a, id="func1"), pytest.param(b, id="func2")]
)
def func1_parametrized(parametrized_name_0, a, b):
    return parametrized_name_0

