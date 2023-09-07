#module with refactoring utilities

from pathlib import Path;
import ast;


def parse_file_to_AST(path : str | Path ) -> ast.AST:
    """Takes a filename, checks validity (.py file, and exists) and 
    returns a complete abstract syntax tree (AST) for the file, from the 'ast' module
    
    Parameters: 
        - path - path to relevant file. str or pathlib.Path

    Returns:
        ast.AST - base of the AST for given python file.
    """
    #error handling
    path = Path(path) #gives valueerror if not a path
    if not path.exists():
        raise ValueError("File does not exist: " + path)
    elif not path.is_file():
        raise IsADirectoryError("Given path points to a directory: " + path)
    elif not len(path.parts[-1]) > 3 and path.parts[-1][-3:] == ".py":
        raise ValueError("Not a python file: " + path)
    
    #opening file
    with open(path) as f:
        parsed_ast = ast.parse(f.read())
    return parsed_ast

def parse_AST_to_file(ast_base: ast.AST, filepath: str | Path):
    """Takes an AST and a filepath, and unparses the given AST into the given file.

    Parameters: 
        - ast_base - base of an AST
        - filepath - path of location to unparse AST. str or pathlib.Path

    Returns:
        None
    """
    path = Path(filepath)    

    string_ast = ast.unparse(ast_base)
    with open(path, "w") as file:
        file.write(string_ast)


def find_clone_nodes_in_AST(ast_base, clone_names):

    clone_nodes = []

    #only for one file
    for i in range(len(ast_base.body)):
        node = ast_base.body[i]
        if isinstance(node, ast.FunctionDef) and node.name in clone_names:
            clone_nodes.append(node)

    return clone_nodes