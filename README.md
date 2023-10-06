# master-refactoring

Run refactoring_test/refactor_type1_clones.py or refactoring_test/refactor_type2_clones.py to test the refactoring (of the test_calculator files in test_files, calculator_type1.py and calculator_type2.py) 


Runs with python 3.10 <=



TODO:


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
@pytest.mark.parametrize('name', ["with_confirmation", "select_command_with_arrows", "refuse_with_confirmation", "without_confirmation"])
def test(proc, TIMEOUT, name):
    eval(name)(proc, TIMEOUT)
```