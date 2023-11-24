# master-refactoring


Runs with python 3.10 <=


Do we have to handle a case with two clones: one parametrized, one not? What would this case look like

TODO:
1. Currently we refactor into the 'first occurence' (whatever nicad gives us first.). Can cause problem with undefined variables

2. requirements.txt

3. when -m/--mark flag is used, add custom mark to pytest.ini file. (How to find pytest.ini file?) Only do this if we want to keep -m

4. Find out what to do with """ comment in top of test

5. "#different argnames should be handled elsewhere, as it should lead to the creation of a NodeDifference object". Investigate...
Doesnt sound right.

-------------------------------------------------------------------------------------------


POTENTIAL BUGS

- When keeping names after they appear on the left side of an assign statement, we don't check whether the assign statement is reached. Preferably, we should only keep names if the assign statement is always executed (not inside an if, loop, etc.)  



OTHER INTERESTING STUFF:

Haven't dealt with this:
```python
import pytest

#this line parametrizes every test in the module (file)
pytestmark = pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])

class TestClass:
    def test_simple_case(self, n, expected):
        assert n + 1 == expected

    def test_weird_simple_case(self, n, expected):
        assert (n * 1) + 1 == expected

```
