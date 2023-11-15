# master-refactoring


Runs with python 3.10 <=


TODO:
1. flag for overwriting/making new file

2. requirements.txt

3. Perhaps create new mark for every test being parametrized? 
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

4. Change os.system to subprocess module

5. FIX THIS: currently, different these aren't clones:
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


BUGS:

- Tests in classes aren't indented as they should be

POTENTIAL BUGS

- When keeping names after they appear on the left side of an assign statement, we don't check whether the assign statement is reached. Preferably, we should only keep names if the assign statement is always executed (not inside an if, loop, etc.)  
