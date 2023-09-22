import ast
from pathlib import Path;

class ASTParser():
    """Class which includes static methods for parsing and unparsing an AST for a file.
    Also does some sanity checks to make sure the file is correct. 
    """
    def parse_file_to_AST(path : str | Path ) -> ast.AST:
        """Takes a filename, checks validity (.py file, and exists) and 
        returns a complete abstract syntax tree (AST) for the file, from the 'ast' module
        
        Parameters: 
            - path - path to relevant file. str or pathlib.Path

        Returns:
            ast.AST - base of the AST for given python file.
        """
        #error handling
        path = Path(path) #gives typerror if not a path
        if not path.exists():
            raise ValueError("File does not exist: " + str(path))
        elif not path.is_file():
            raise IsADirectoryError("Given path points to a directory: " + path)
        elif not len(path.parts[-1]) > 3 and path.parts[-1][-3:] == ".py":
            raise ValueError("Not a python file: " + path)
        
        #opening file
        with open(path) as f:
            parsed_ast = ast.parse(f.read())
        return parsed_ast


    def parse_AST_to_file(ast_base, filepath: str | Path):
        """Takes an AST and a filepath, and unparses the given AST into the given file.

        Parameters: 
            - ast_base - base of an AST from 'ast' module
            - filepath - path of location to unparse AST. str or pathlib.Path

        Returns:
            None
        """
        path = Path(filepath).resolve()

        string_ast = ast.unparse(ast_base)
        with open(path, "w") as file:
            file.write(f'{string_ast}')