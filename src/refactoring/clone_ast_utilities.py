# module which has utility functions for finding clones in AST and removing clones from AST.

import ast


class CloneASTUtilities:
    """Includes a set of static functions to find clones and compare clones"""

    def find_clone_node_in_AST(ast_base, clone_lineno: int, filehandler):
        """For a single clone, finds AST-node of clone based on line number of function definition.


        Parameters:
            - ast_base - base of an AST from 'ast' module
            - clone_lineno - list of lists of clone pairs in AST, identified by function names
            TODO: add rest

        Returns:
            A single Clone object, representing the clone found at given line number.
        """

        # import here, otherwise circular import
        from .clone import Clone

        # only for one file
        for node in ast_base.body:
            if isinstance(node, ast.FunctionDef) and node.lineno == clone_lineno:
                return Clone(node, parent_node=ast_base, lineno=node.lineno, filehandler=filehandler)
            elif isinstance(node, ast.ClassDef):
                for class_node in node.body:
                    if (isinstance(class_node, ast.FunctionDef) and class_node.lineno == clone_lineno):
                        return Clone(class_node, parent_node=node, lineno=class_node.lineno, filehandler=filehandler)


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


    def get_all_descendants(node):
        for child in ast.iter_child_nodes(node):
            yield child
            yield from CloneASTUtilities.get_all_descendants(child)

    def has_import_statement(ast_base):
        for stmt in ast_base.body:
            if type(stmt) == ast.Import:
                if len(stmt.names) == 1 and stmt.names[0].name == "pytest":
                    return True
        return False
                        
    def get_import_statement():
        return ast.Import(names=[ast.alias(name="pytest")])

    def get_mark_decorator(mark_name="parametrize_refactored"):
        return ast.Attribute(
            value=ast.Attribute(
                value=ast.Name(
                    id="pytest"
                ),
                attr="mark"),
            attr=mark_name)
