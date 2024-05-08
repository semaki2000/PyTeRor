import ast
#from black import FileMode, format_str
from pathlib import Path;
from .unparser import Unparser
from .clone_ast_utilities import CloneASTUtilities

class ASTParser():
    """Class which includes static methods for parsing and unparsing an AST for a file.
    Also does some sanity checks to make sure the file is correct, 
    in addition to formatting the pytest.mark.parametrize decorator line.
    """
    tests = 0
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
            try:
                parsed_ast = ast.parse(f.read())
            except:
                return False
        return parsed_ast


    def parse_AST_to_file(ast_base, filepath: str | Path):
        """Takes an AST and a filepath, and unparses the given AST into the given file, using the ast-subclass Unparser.

        Parameters: 
            - ast_base - base of an AST from 'ast' module
            - filepath - path of location to unparse AST. str or pathlib.Path

        Returns:
            None
        """
        path = Path(filepath).resolve()

        target_sc = Unparser._unparse(ast_base) 
        #target_sc = ASTParser.format_parametrize_decorator(target_sc)
        with open(path, "w+") as file:
            file.write(f'{target_sc}')


    def count_tests(path: str | Path):
        path = Path(path).resolve()

        for file in [str(file) for file in path.rglob('*') if file.is_file()]:
            parsed_ast = ASTParser.parse_file_to_AST(file)
            
            if type(parsed_ast) == ast.Module:
                ASTParser.tests += CloneASTUtilities.count_tests(parsed_ast)

    
    #--- no longer used ---
    #change from source code analysis to going through AST
    #needs to be done here:
    #   strings which have explicit \n in them need to be changed to multiline strings
    #   args of pytest.mark.parametrize need to be newlined, so there isnt just one long line
    def format_parametrize_decorator(source_code):
        code_lines = source_code.split('\n') 

        for line_ind in range(len(code_lines)):
            if '@pytest.mark.parametrize(' in code_lines[line_ind]:
                code_lines[line_ind] = "@pytest.mark.parametrize"
        return '\n'.join(code_lines) 