# master-refactoring


## Installation 

1. clone repository

2. Install nicad.

3. Copy file 'python.grm' into txl sub-directory in nicad directory. E.g. 'sudo cp python.grm /use/local/lib/nicad6/txl/python.grm'

4. Copy file 'type2_abstracted.cfg' into config sub-directory in nicad directory. E.g. 'sudo cp type2_abstracted.cfg /use/local/lib/nicad6/config/type2_abstracted.cfg'. 

Runs with python 3.10 <=


## TODO

1. Currently we refactor into the 'first occurence' (whatever nicad gives us first.). Can cause problem with undefined variables. Better idea to refactor into last occuring clone?

2. when -m/--mark flag is used, add custom mark to pytest.ini file. (How to find pytest.ini file?) Only do this if we want to keep -m

3. Docstring: Add docstrings back into top of function body, prepend which test the docstring is from. All should still be in one string. Ex:
"""test_name:
DOCSTRING CONTENT OF TEST_NAME
   test_name2:
DOCSTRING CONTENT OF TEST_NAME2
"""

4. "#different argnames should be handled elsewhere, as it should lead to the creation of a NodeDifference object". Investigate...
Doesnt sound right.

5. Tests can have multiple parametrize decorators. Currently only one is accounted for. 
Turn clone.param_decorator into list of objects, rather than single object

6. Related to above, handle this case:
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


POTENTIAL BUGS

- When keeping names after they appear on the left side of an assign statement, we don't check whether the assign statement is reached. Preferably, we should only keep names if the assign statement is always executed (not inside an if, loop, etc.)  


