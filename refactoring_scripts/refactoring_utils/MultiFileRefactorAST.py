from .RefactorAST import RefactorAST
from .NameGenerator import NameGenerator
from pathlib import Path

class MultiFileRefactorAST(RefactorAST):
    def __init__(self, filepaths : str | Path | list, new_var_name="new_var"):
        """Class which includes some useful methods for refactoring code clones.
        
        Parameters: 
            - filepaths - path to relevant file(s). Single filepath (given as str or Path), or a list of filepaths (same types).
            - new_var_name (optional) - Name of new variables which are created when differences are lifted out of clone functions.
                Defaults to "new_var", giving names like "new_var_0", "new_var_1".

        """
        
        if type(filepaths) == list:
            self.ast_base = []
            for path in filepaths:
                self.ast_base.append(parse_file_to_AST(path))
        else:
            self.ast_base = self.parse_file_to_AST(filepaths)
        self.name_gen = NameGenerator(new_var_name)