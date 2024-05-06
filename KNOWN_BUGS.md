# KNOWN BUGS

Multiline strings can be wrongly indented after refactoring (only if test is in a class):
```python
#pre-refactoring
    def test_to_records_with_inf_as_na_record(self):
        # GH 48526
        expected = """   NaN  inf         record
0  inf    b    [0, inf, b]
1  NaN  NaN  [1, nan, nan]
2    e    f      [2, e, f]"""
        msg = "use_inf_as_na option is deprecated"
        with tm.assert_produces_warning(FutureWarning, match=msg):
            with option_context("use_inf_as_na", True):
                df = DataFrame(
                    [[np.inf, "b"], [np.nan, np.nan], ["e", "f"]],
                    columns=[np.nan, np.inf],
                )
                df["record"] = df[[np.nan, np.inf]].to_records()
                result = repr(df)
        assert result == expected

#post-refactoring
    @pytest.mark.parametrize(
        "parametrized_constant_0",
        [
            pytest.param(True, id="test_to_records_with_inf_as_na_record"),
            pytest.param(False, id="test_to_records_with_inf_record"),
        ],
    )
    @pytest.mark.parametrize_refactored
    def test_to_records_with_inf_as_na_record_parametrized(self, parametrized_constant_0):
        expected = """   NaN  inf         record
    0  inf    b    [0, inf, b]
    1  NaN  NaN  [1, nan, nan]
    2    e    f      [2, e, f]"""
        msg = "use_inf_as_na option is deprecated"
        with tm.assert_produces_warning(FutureWarning, match=msg):
            with option_context("use_inf_as_na", parametrized_constant_0):
                df = DataFrame(
                    [[np.inf, "b"], [np.nan, np.nan], ["e", "f"]], columns=[np.nan, np.inf]
                )
                df["record"] = df[[np.nan, np.inf]].to_records()
                result = repr(df)
        assert result == expected
```