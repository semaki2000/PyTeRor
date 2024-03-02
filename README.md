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

handle this: 

pytest.mark.parametrize(argnames='axis', argvalues=[None, 1, (1,), (0, 1), (-3, -1)])
(keywords)

0. When extracting differences that are names, check if names are parameters. If so, replace them in suite and definition with generated identifier.

1. Currently we refactor into the 'first occurence' (whatever nicad gives us first.). Can cause problem with undefined variables. Better idea to refactor into last occuring clone?

2. when -m/--mark flag is used, add custom mark to pytest.ini file. (How to find pytest.ini file?) Only do this if we want to keep -m

3. "#different argnames should be handled elsewhere, as it should lead to the creation of a NodeDifference object". Investigate...
Doesnt sound right.

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

6. Find the pytest.ini file (if it exists) (eventually hidden .pytest.ini) (eventually eventually a pyproject.toml with [tool.pytest.ini_options]).
Example of pytest.ini:
```ini
# content of pytest.ini
# Example 1: have pytest look for "check" instead of "test"
[pytest]
python_files = check_*.py
python_classes = Check
python_functions = *_check
norecursedirs = #dirs with files that should not tested. Should therefore not be copied in copytree
testpaths = #if no arguments in CL, testpaths that should be recursed through to find tests. These need to be  
``` 
7. Add a #TODO comment over refactored tests? for renaming. probably, dont.
-------------------------------------------------------------------------------------------


POTENTIAL BUGS

- When keeping names after they appear on the left side of an assign statement, we don't check whether the assign statement is reached. Preferably, we should only keep names if the assign statement is always executed (not inside an if, loop, etc.)
- f-strings (literals that are in f-string, but dont have them as direct parent)

-decorators inside inner functions inside our test functions... ignored by nicad, not by ast module
 
