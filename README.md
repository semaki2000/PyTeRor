# master-refactoring


## Installation 

1. clone repository

2. Install requirements (pip install -r requirements.txt).

3. Install nicad.

4. Copy file 'python.grm' into txl sub-directory in nicad directory. E.g. 'sudo cp python.grm /usr/local/lib/nicad6/txl/python.grm'

5. Run makefile in nicad directory.

5. Copy file 'type2_abstracted.cfg' into config sub-directory in nicad directory. E.g. 'sudo cp type2_abstracted.cfg /usr/local/lib/nicad6/config/type2_abstracted.cfg'. 

Runs with python 3.10 <=


## TODO


1. Currently we refactor into the 'first occurence' (whatever nicad gives us first.). Can cause problem with undefined variables. Better idea to refactor into last occuring clone?


4. Handle this case:
```python
import pytest

#this line parametrizes every test in the module (file)
#assigns to the pytestmark global variable
pytestmark = pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])
#can also be assignment to a list of marks, e.g:
#pytestmark = [pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)]), pytest.mark.example_mark]

class TestClass:
    def test_simple_case(self, n, expected):
        assert n + 1 == expected

    def test_weird_simple_case(self, n, expected):
        assert (n * 1) + 1 == expected
```
Do this by:
    a. finding pytestmark line. This has to be done in filehandler, on a file by file basis.
    b. For each mark m in pytestmark:
        i. If parametrize, create ParametrizeDecorator object and parse m. Add object to all clones in file. (clone.param_decorator.append(m))
        ii. Else, if regular mark, add to clone.marks for every clone.
        iii. If fixture (is this possible?), set is_fixture to True for every clone in file.

-------------------------------------------------------------------------------------------


KNOWN BUGS

 
-multiline strings can be wrongly indented after refactoring (only if test is in a class):

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