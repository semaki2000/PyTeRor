#module with refactoring utilities

import pathlib;
import ast;


def parse_file_to_AST(filename):
    with open("../test_files/calculator_test_type1clone.py") as f:
        parsed_ast = ast.parse(f.read())
    return parsed_ast

def parse_AST_to_file(ast_tree, filename: str):
    
    string_ast = ast.unparse(ast_tree)
    with open(filename, "w") as file:
        file.write(string_ast)


def find_clone_nodes_in_AST(ast_tree, clone_names):

    clone_nodes = []

    #only for one file
    for i in range(len(ast_tree.body)):
        node = ast_tree.body[i]
        if isinstance(node, ast.FunctionDef) and node.name in clone_names:
            clone_nodes.append(node)

    return clone_nodes