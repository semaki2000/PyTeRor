
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
        if self.ast_node.col_offset != 0:
            #prepend 'class' so it can be correctly formatted by black.
            #black will not format indented code, syntactically incorrect.
            class_prepend = "class A:\n"
            indented_str_target_sc = ""
                
            for line in str_target_sc.split('\n'):
                #we multiply with ast_node.col_offset attribute, to get indent level
                indented_line = (" " * self.ast_node.col_offset) + line + "\n"
                indented_str_target_sc += indented_line

            str_target_sc = class_prepend + indented_str_target_sc

        formatted = ""
        match (self.formatter):
            case "black":
                formatted = self.black_format_target(str_target_sc, line_length=line_length)
                
            case _:
                formatted = str_target_sc
                
            #NOTE: could add more formatters here if needed.
        if self.ast_node.col_offset != 0:
            formatted = formatted.replace(class_prepend, '', 1)

        return formatted

    def black_format_target(self, source, line_length):
        BLACK_MODE = black.Mode(target_versions={black.TargetVersion.PY311}, line_length=line_length)
        formatted_target = black.format_file_contents(source, fast=False, mode=BLACK_MODE)
        return formatted_target        