# master-refactoring


Runs with python 3.10 <=



TODO:


- fix bug with same name appearing multiple times in .parametrize args, if used multiple times in test:
```python
@pytest.mark.parametrize('parametrized_constant_0, parametrized_name_0', [('', transform, transform), ('', transform, transform), ('', boolean, boolean)])
```


- Given that we refactor names: NodeDifference class should have a boolean whether the node is unconditional or conditional. (control flow)

- How to handle this?
```python
from a import TRANSFORM_FUNCTIONS #tuple defined elsewhere

@pytest.mark.parametrize("transform", TRANSFORM_FUNCTIONS) #then used in annotation
def test_...():
```

- Parametrize attributes? (Probably not a good idea, but can potentially be done using get_attr)

- 'import pytest' into source code if not imported in source already (only if changes are made to file)

- Problems with pre-existing decorators in clones...
    - If there is a .parametrize decorator in all clones, put in target... Else:
    - Give a warning that the refactoring could be wrong when dealing with decorators/annotations? (except .parametrize)
Example of above problem (from ERT-repo):
```python
@pytest.mark.parametrize("transform", TRANSFORM_FUNCTIONS)
def test_output_transform_is_gotten_from_keyword(parse_field_line, transform):
    field = parse_field_line(
        f"FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl OUTPUT_TRANSFORM:{transform}"
    )
    assert field.output_transformation == transform


@pytest.mark.parametrize("transform", TRANSFORM_FUNCTIONS)
def test_init_transform_is_gotten_from_keyword(parse_field_line, transform):
    field = parse_field_line(
        f"FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl INIT_TRANSFORM:{transform}"
    )
    assert field.input_transformation == transform

@pytest.mark.parametrize("boolean", [True, False])
def test_forward_init_is_gotten_from_keyword(parse_field_line, boolean):
    if ():
        field = parse_field_line(
        f"FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl FORWARD_INIT:{boolean}"
    )
    assert field.forward_init == boolean
```


- Figure out when names need to be extracted, and when they dont. Idea: if it appears on left side of assign during the test, it won't have to be extracted? Only the case if it isn't potentially unreached code. Eventually, extract all names anyway. Example:
```python

#names can safely be ignored here, 
def test_name1():
    var_name = "aaa"
    assert var_name == "aaa"

def test_name2():
    different_var_name = "bbb"
    assert different_var_name == "bbb"

#refactored into ->
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

#refactored into -> 
@pytest.mark.parametrize("name, constant", [(var_name, "aaa"), (different_var_name, "bbb")])
def test_parametrized(constant):
    name = constant
    assert name == constant

#How much precaution of things defined outside scope should we take?
```

get_attr(obj, "a")

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

- Find out what to do with clones between files (probably best to ignore).




POTENTIAL BUGS

- When keeping names after they appear on the left side of an assign statement, we don't check whether the assign statement is reached. Preferably, we should only keep names if the assign statement is always executed (not inside an if, loop, etc.)  
