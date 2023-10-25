class ParametrizedArg:
    """Class representing the name and values of a single parameter in the pytest.mark.parametrize decorator.
    Example:

    ```python
    @pytest.mark.parametrize("argname1, argname2", [("a", 1), ("b", 2)])
    ```
    This line has two ParametrizedArg objects: 
    - one with argname="argname1", and values=["a", "b"].
    - the other with argname="argname2", and values=[1, 2]
       """
    def __init__(self, argname : str):
        self.argname = argname
        self.values = []
        print("created obj with argname:", self.argname)

    def add_value(self, value):
        self.values.append(value)
        print("added value:", value, "to argname:", self.argname)

