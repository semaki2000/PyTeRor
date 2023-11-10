# master-refactoring


Runs with python 3.10 <=


TODO:
1. Pre-existing decorators, non-pytest.
    If all clones have the same decorator, no problem
    Otherwise, split off clones with the same decorator into new clone class.

2. flag for overwriting/making new file

3. requirements.txt

4. Perhaps create new mark for every test being parametrized? 
This could imitate functionality of 'pytest -k test_name'
It would instead be 'pytest -m test_name:
```python
@pytest.mark.parametrize("new_var", [
    pytest.param("A", marks=pytest.mark.test_a, id="test_a"),
    pytest.param("B", marks=pytest.mark.test_b, id="test_b"),
])
def test_a_parametrized(new_var):
    assert new_var
```

5. Change os.system to subprocess module

6. FIX THIS: currently, different these aren't clones:
```python

@pytest.mark.test
@pytest.mark.usefixtures("a")
def test_this():
    pass



@pytest.mark.usefixtures("a")
def test_that():
    pass    

```
Test in test_files/test_clone_detection_and_refactoring/test_lark_parser.py
-------------------------------------------------------------------------------------------


- How to handle this? Anwer: probably don't, edge case
```python
from a import TRANSFORM_FUNCTIONS #list of tuples defined elsewhere

@pytest.mark.parametrize("transform", TRANSFORM_FUNCTIONS) #then used in annotation
def test_...():
```
Potential theoretical answer to above could be with tuple unpacking of some sort
But gets a bit complicated


- How to name new generated test? User input? Related to:
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

new annotation?? 

- Parsing and unparsing from AST gives lots of formatting problems:
    - All pre-existing whitespace and formatting is removed in whole file
    - the .parametrize line can become very long, needs to be divided into multiple lines.
    - Potential solutions: 
        - use a formatter (black, yapf). Problem again: different formatting than original file
        - Only use ast.unparse() for the clones. keep original file as much as possible, just remove lines with clones and replace with ast.unparse() output



POTENTIAL BUGS

- When keeping names after they appear on the left side of an assign statement, we don't check whether the assign statement is reached. Preferably, we should only keep names if the assign statement is always executed (not inside an if, loop, etc.)  
