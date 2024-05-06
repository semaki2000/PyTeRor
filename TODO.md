## TODO

Currently we refactor into the 'first occurence' (whatever nicad gives us first.). Could cause problem with undefined variables? Better idea to refactor into last occuring clone? Investigate


Handle this case?
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
If so, Do this by:
    a. finding pytestmark line. This has to be done in filehandler, file by file basis.
    b. For each mark m in pytestmark:
        i. If parametrize, create ParametrizeDecorator object and parse m. Add object to all clones in file. (clone.param_decorator.append(m))
        ii. Else, if regular mark, add to clone.marks for every clone.
        iii. If fixture (is this possible?), set is_fixture to True for every clone in file.

-------------------------------------------------------------------------------------------

