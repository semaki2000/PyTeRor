# master-refactoring


Runs with python 3.10 <=



TODO:

- write extract_differences function to handle names on left side of assignment (using NameNodeDifference class)

- find a better way to parametrize attribute, if any (better than get_attr())

- import pytest if not imported in source already (only if changes are made)

- If decorator in all clones, put in target... Else:
- Give a warning that the refactoring could be wrong when dealing with decorators/annotations? (except .parametrize)

- Figure out when names need to be extracted, and when they dont. Idea: if it appears on left side of assign during the test, it won't have to be extracted? Only the case if it isn't potentially unreached code. Eventually, extract all names anyway. Example:
```python

#names can safely be ignored here, 
def test_name1():
    var_name = "aaa"
    assert var_name == "aaa"

def test_name2():
    different_var_name = "bbb"
    assert different_var_name == "bbb"

@pytest.mark.parametrize("constant", [("aaa"), ("bbb")])
def test_parametrized(constant):
    var_name = constant
    assert var_name == constant


#######################################

#names could be defined outside scope of test here, 
# therefore have to be extracted into parametrize decorator

def test_name1():
    assert var_name == "aaa"

def test_name2():
    assert different_var_name == "bbb"

@pytest.mark.parametrize("name, constant", [(var_name, "aaa"), (different_var_name, "bbb")])
def test_parametrized(constant):
    name = constant
    assert name == constant

```


- Parse the xml file (if we keep nicad)

- Handle tests in classes. Also clone classes where some tests are in different test classes (clone class must be split). Example, where two clones are in different test classes should not be parametrized:

```python
class A:
    def test_name1():
        assert name1 == "aaa"
class B:
    def test_name2():
        assert name2 == "bbb"
```
- How to name new generated test? User input?
- Problem with name of test being lost when parametrizing. Maybe try using markers when parametrizing functions in order to keep info on old function names? For example:
```python
def test_name1():
    assert name1 == "aaa"

def test_name2():
    assert name2 == "bbb"

#Add markers by f.ex replacing each individual set of args run with pytest.param, 
# with keyword 'marks' set to old name of test? New marks must then be added in pytest.ini file
@pytest.mark.parametrize("name", (
                             pytest.param(name1, marks=pytest.mark.test_name1),
                             pytest.param(name2, marks=pytest.mark.test_name2)
                             ))
def test_(name): #what to call the refactored test? keep one of the old names? generate name?
    assert name == "aaa"

```
- Fix the stuff with .parametrize() (there can be multiple parametrize decorators, also result probably shouldn't be cartesian product)

- Parsing and unparsing from AST gives lots of formatting problems:
    - All pre-existing whitespace and formatting is removed in whole file
    - the .parametrize line can become very long, needs to be divided into multiple lines.
    - Potential solutions: 
        - use a formatter (black, yapf). Problem again: different formatting than original file
        - Only use ast.unparse() for the clones. keep original file as much as possible, just remove lines with clones and replace with ast.unparse() output

- Find out what to do with clones between files (probably best to ignore).