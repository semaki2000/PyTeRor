import ast

class DecoratorChecker:
    def is_parametrize_decorator(decorator):
        """Checks whether a given node is a pytest.mark.parametrize decorator.

        Params:
            - decorator - AST-node of decorator to check.

        Returns:
            boolean
        """

        # parametrize call, lots of if-s to avoid errors with other decorators
        if type(decorator) == ast.Call and type(decorator.func) == ast.Attribute:
            # if over mutiple lines for "readability"
            if type(decorator.func.value) == ast.Attribute:
                if type(decorator.func.value.value) == ast.Name:
                    if (
                        decorator.func.value.value.id == "pytest"
                        and decorator.func.value.attr == "mark"
                        and decorator.func.attr == "parametrize"
                    ):
                        return True
        return False

    def is_fixture_decorator(decorator):
        """Checks whether a given node is a pytest.fixture decorator.

        Params:
            - decorator - AST-node of decorator to check.

        Returns:
            boolean
        """
        # parametrize call, lots of if-s to avoid errors with other decorators
        if type(decorator) == ast.Call and type(decorator.func) == ast.Attribute:
            # fixture with params (fixture as call)
            if (
                type(decorator.func.value) == ast.Name
                and decorator.func.value.id == "pytest"
                and decorator.func.attr == "fixture"
            ):
                return True
        # simple fixture (no call, only attribute)
        elif (
            type(decorator) == ast.Attribute
            and type(decorator.value) == ast.Name
            and decorator.value.id == "pytest"
            and decorator.attr == "fixture"
        ):
            return True
        return False
    
    def is_mark_decorator(decorator):
        """Checks whether a given node is a pytest.mark... decorator.

        Params:
            - decorator - AST-node of decorator to check.

        Returns:
            boolean
        """

        # simple pytest.mark (no call, only nested attributes)
        if (
            type(decorator) == ast.Attribute
            and type(decorator.value) == ast.Attribute
            and type(decorator.value.value) == ast.Name
            and decorator.value.value.id == "pytest"
            and decorator.value.attr == "mark"
            and isinstance(decorator.attr, str) 
        ):
            return True


        #can also be 
        if type(decorator) == ast.Call and type(decorator.func) == ast.Attribute:
            # mark with params (mark as call)
            if (
                type(decorator.func.value) == ast.Attribute
                and type(decorator.func.value.value) == ast.Name
                and decorator.func.value.value.id == "pytest"
                and decorator.func.value.attr == "mark"
            ):
                return True
        
        return False

    def is_any_pytest_decorator(decorator):
        """Checks whether a given node is a pytest.mark... decorator.

        Params:
            - decorator - AST-node of decorator to check.

        Returns:
            boolean
        """
        unparsed = ast.unparse(decorator)
        if unparsed[:6] == "pytest":
            return True
        return False