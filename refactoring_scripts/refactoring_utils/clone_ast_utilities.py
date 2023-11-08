# module which has utility functions for finding clones in AST and removing clones from AST.

import ast


class CloneASTUtilities:
    """Includes a set of static functions to find clones and compare clones"""

    def find_clone_node_in_AST(ast_base, clone_lineno: int):
        """For a single clone, finds AST-node of clone based on line number of function definition.


        Parameters:
            - ast_base - base of an AST from 'ast' module
            - clone_lineno - list of lists of clone pairs in AST, identified by function names

        Returns:
            A single Clone object, representing the clone found at given line number.
        """

        # import here, otherwise circular import
        from .clone import Clone

        # only for one file
        for node in ast_base.body:
            if isinstance(node, ast.FunctionDef) and node.lineno == clone_lineno:
                return Clone(node, parent_node=ast_base, lineno=node.lineno)
            elif isinstance(node, ast.ClassDef):
                for class_node in node.body:
                    if (isinstance(class_node, ast.FunctionDef) and class_node.lineno == clone_lineno):
                        return Clone(class_node, parent_node=node, lineno=class_node.lineno)

    def detach_redundant_clones(ast_base, redundant_clones: list):
        """Detaches given nodes from the AST.

        Parameters:
            - ast_base - base of an AST from 'ast' module
            - redundant_clones - list of ast nodes which are redundant clones (already parameterized)

        Returns:
            None
        """
        for node in redundant_clones:
            ast_base.body.remove(node)

    def replace_node(child, parent, new_child):
        """Replaces one node with another in the AST.

        Parameters:
            - child - original child, to be replaced
            - parent - parent node of child.
            - new_child - new child, which will replace 'child'

        Returns:
            None
        """
        for attribute in parent._fields:
            # if attr is a list, try to find in list
            if type(getattr(parent, attribute)) == list:
                attr_list = getattr(parent, attribute)
                try:
                    ind = attr_list.index(child)
                    attr_list.pop(ind)
                    attr_list.insert(ind, new_child)
                except ValueError:
                    pass  # wrong attr
            else:
                # not list, value can simply be overwritten
                if getattr(parent, attribute) == child:
                    setattr(parent, attribute, new_child)

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

    def get_eval_call_node(arg):
        func_name = ast.Name(id="eval")
        eval_node = ast.Call(func=func_name, args=[arg], keywords=[])
        return eval_node

    def get_getattr_call_node(arg):
        func_name = ast.Name(id="getattr")
        getattr_node = ast.Call(func=func_name, args=[arg], keywords=[])
        return getattr_node
