@pytest.mark.parametrize(
    "dtype, expected",
    [(Float32Dtype(), "Float32Dtype()"), (Float64Dtype(), "Float64Dtype()")],
)
def test_repr_dtype(dtype, expected):
    assert repr(dtype) == expected


def test_next_workday(day, expected):
    assert next_workday(day) == expected


