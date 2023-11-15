
import black
from .unparser import Unparser

class TargetFormatter():

    def __init__(self, ast_node, lineno, indent = False, formatter="black") -> None:
        self.ast_node = ast_node
        self.lineno = lineno
        self.formatter = formatter

    def format_target(self, line_length = 100):
        """Formats the unparsed ast of the target with a formatter(currently: 'black' formatter),
        then returns the formatted code as a list of strings (one element per line of code)"""
        str_target_sc = Unparser._unparse(ast_node=self.ast_node)
        match (self.formatter):
            case "black":
                return self.black_format_target(str_target_sc, line_length=line_length)
            case _:
                return str_target_sc
            
            #NOTE: could add more formatters here if needed.
    
    def black_format_target(self, source, line_length):
        BLACK_MODE = black.Mode(target_versions={black.TargetVersion.PY311}, line_length=line_length)
        formatted_target = black.format_file_contents(source, fast=False, mode=BLACK_MODE)
        return formatted_target        