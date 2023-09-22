#module which has utility functions for finding clones in AST and removing clones from AST.

import ast;
from .clone import Clone


class CloneASTUtilities():
    """Includes a set of static functions to find clones and compare clones"""

    def find_clone_node_in_AST(ast_base, clone_lineno: int):
        """For a single clone, finds AST-node of clone based on line number of function definition.


        Parameters: 
            - ast_base - base of an AST from 'ast' module
            - clone_lineno - list of lists of clone pairs in AST, identified by function names

        Returns:
            List of lists of ast-nodes, with all ast-nodes in the same list being clones with each other.
        """


        #only for one file
        for node in ast_base.body:
            if isinstance(node, ast.FunctionDef) and node.lineno == clone_lineno:
                return Clone(node, ast_base, node.lineno)


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
            
