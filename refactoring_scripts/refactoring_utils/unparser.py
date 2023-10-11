import ast

#source: https://stackoverflow.com/questions/72542556/using-python-ast-parser-to-process-multi-line-strings
class Unparser(ast._Unparser):
    def visit_Constant(self, node):
        if isinstance(node.value, str):# and node.lineno < node.end_lineno:
            super()._write_str_avoiding_backslashes(node.value)
            return
        return super().visit_Constant(node)

    def _unparse(ast_node):
        u = Unparser()
        return u.visit(ast_node)