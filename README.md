# master-refactoring


To install: 

1. clone repository

2. Install nicad.

3. Copy file 'python.grm' into txl sub-directory in nicad directory. E.g. 'sudo cp python.grm /use/local/lib/nicad6/txl/python.grm'

4. Copy file 'type2_abstracted.cfg' into config sub-directory in nicad directory. E.g. 'sudo cp type2_abstracted.cfg /use/local/lib/nicad6/config/type2_abstracted.cfg'. 

Runs with python 3.10 <=


Do we have to handle a case with two clones: one parametrized, one not? What would this case look like
-> pytest requires all parameters to either be in parametrize, or be a fixture.

TODO:
0. Nicad sees None as a name, not a literal.

1. Currently we refactor into the 'first occurence' (whatever nicad gives us first.). Can cause problem with undefined variables

2. when -m/--mark flag is used, add custom mark to pytest.ini file. (How to find pytest.ini file?) Only do this if we want to keep -m

3. Find out what to do with """ comment in top of test. We have it saved in Clone object if it exists... add it back?

4. "#different argnames should be handled elsewhere, as it should lead to the creation of a NodeDifference object". Investigate...
Doesnt sound right.

5. We want to use a modified version of nicad6's type2 config. How do we do this. When running nicad, for config option it only takes config files that exist in its config/ subfolder. Supplying an external config file doesn't seem to be an option.

6. Remove redundant parameters from funcdef:
```python
def func1(a, b):
    return a

def func2(a, b):
    return b

"""BECOMES""":
@pytest.mark.parametrize(
    "parametrized_name_0", [pytest.param(a, id="func1"), pytest.param(b, id="func2")]
)
def func1_parametrized(parametrized_name_0, a, b): #remove a, b
    return parametrized_name_0    

```
-------------------------------------------------------------------------------------------


POTENTIAL BUGS

- When keeping names after they appear on the left side of an assign statement, we don't check whether the assign statement is reached. Preferably, we should only keep names if the assign statement is always executed (not inside an if, loop, etc.)  



OTHER INTERESTING STUFF:

Haven't dealt with this:
```python
import pytest

#this line parametrizes every test in the module (file)
#assigns to the pytestmark global variable
pytestmark = pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])

class TestClass:
    def test_simple_case(self, n, expected):
        assert n + 1 == expected

    def test_weird_simple_case(self, n, expected):
        assert (n * 1) + 1 == expected

```
