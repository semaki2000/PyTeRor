# master-refactoring


Runs with python 3.10 <=


TODO:
1. add 'import pytest' to refactored source file if not there already

2. Add function to split off a clone class from another
    Could be useful if f.ex. 3 tests, where two are in one test class, and one is in another. (the two tests are parametrized, last is ignored)
    Or if two tests have the same attribute, while another one is different. (first two parametrized, last ignored)

3. Add functionality to CloneASTUtilities to find nodes that are in a class (in function find_clone_node_in_AST). 
    Currently, only finds top-level nodes (looks through body of AST base)
    Finding tests that are children nodes of nodes that aren't classes is probably not necessary.

4. Add functionality to stop refactoring of a clone class if there is a difference in attribute.
    F.ex. CloneClass.get_clone_differences could return a boolean whether the refactoring should continue.

5. Pre-existing decorators, non-pytest.
    If all clones have the same decorator, no problem
    Otherwise, split off clones with the same decorator into new clone class.

6. (Maybe) Create NodeDifference subclass for Attribute differences. Not used for refactoring, but useful for splitting classes (as mentioned above, 2)

7. Implement argparse in main method, makes parsing arguments and adding flags easier.

8. Only unparse test, keep original file. Format refactored code?

10. flag for overwriting/making new file


- Given that we refactor names: NodeDifference class should have a boolean whether the node is unconditional or conditional. (control flow)


- How to handle this? Anwer: probably don't, edge case
```python
from a import TRANSFORM_FUNCTIONS #tuple defined elsewhere

@pytest.mark.parametrize("transform", TRANSFORM_FUNCTIONS) #then used in annotation
def test_...():
```


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
