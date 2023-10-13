# master-refactoring

Run refactoring_test/refactor_type1_clones.py or refactoring_test/refactor_type2_clones.py to test the refactoring (of the test_calculator files in test_files, calculator_type1.py and calculator_type2.py) 


Runs with python 3.10 <=



TODO:

- Problem with name of test being lost when parametrizing. Maybe try using markers when parametrizing functions in order to keep info on old function names? For example:
```python
def test_name1():
    assert name1 == "aaa"

def test_name2():
    assert name2 == "bbb"

#Add markers by f.ex replacing each individual set of args run with pytest.param, with keyword 'marks' set to old name of test? New marks must then be added in pytest.ini file
@pytest.mark.parametrize("name", (
                             pytest.param(name1, marks=pytest.mark.test_name1),
                             pytest.param(name2, marks=pytest.mark.test_name2)
                             ))
def test_(name): #another problem, what to call the refactored test? keep one of the old names? generate name?
    assert name == "aaa"

```
- Fix the stuff with .parametrize() (there can be multiple parametrize decorators, also result probably shouldn't be cartesian product)

- Parsing and unparsing from AST gives lots of formatting problems:
    - All pre-existing whitespace and formatting is removed
    - the .parametrize line can become very long, needs to be divided into multiple lines.
    - Potential solutions: use a formatter (black, yapf).

- Find out what to do with clones between files (probably best to ignore)