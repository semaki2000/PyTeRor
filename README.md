# master-refactoring

Run refactoring_test/refactor_type1_clones.py or refactoring_test/refactor_type2_clones.py to test the refactoring (of the test_calculator files in test_files, calculator_type1.py and calculator_type2.py) 


Runs with python 3.10 <=



TODO:

- Maybe try using markers when parametrizing functions in order to keep info on old function names?
For example:
```python
def test_name1():
    assert name1 == "aaa"

def test_name2():
    assert name2 == "bbb"

#Add markers by f.ex replacing each individual set of args run with pytest.param, with keyword 'marks' set to old name of test?
@pytest.mark.parametrize("name", (
                             pytest.param(name1, marks=pytest.mark.test_name1),
                             pytest.param(name2, marks=pytest.mark.test_name2)
                             ))
def test_(name): #another problem, what to call the refactored test? keep one of the old names? generate name?
    assert name == "aaa"

```
- Fix the stuff with .parametrize() (there can be multiple parametrize decorators, also result probably shouldn't be cartesian product)

- Change eval(STRING) to extract name into parametrize decorator instead.
- Find out what to do with clones between files (probably best to ignore)

- Find out how to handle stuff like this:

```python


def test_with_confirmation(proc, TIMEOUT):
    with_confirmation(proc, TIMEOUT)


def test_select_command_with_arrows(proc, TIMEOUT):
    select_command_with_arrows(proc, TIMEOUT)


def test_refuse_with_confirmation(proc, TIMEOUT):
    refuse_with_confirmation(proc, TIMEOUT)


def test_without_confirmation(proc, TIMEOUT):
    without_confirmation(proc, TIMEOUT)


#COULD be refactored into:
@pytest.mark.parametrize('name', [with_confirmation, select_command_with_arrows, refuse_with_confirmation, without_confirmation])
def test(proc, TIMEOUT, name):
    name(proc, TIMEOUT)
```