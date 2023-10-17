from .node_difference import NodeDifference
from .clone_ast_utilities import CloneASTUtilities
import ast

class ConstantNodeDifference(NodeDifference):

    def __init__(self, nodes, parent_nodes):
        super().__init__(nodes, parent_nodes)
        self.stringtype = "constant"

    
    
    def __str__(self):
        ret = []
        for node in self.nodes:
            ret.append(node.value)
        return str(ret)
    
    def in_fstring(self):
        if type(self.parent_nodes[0]) == ast.JoinedStr:
            return True
        return False

    #override parent class
    def replace_nodes(self, parametrized_name):
        if self.in_fstring():
            replace_node = ast.FormattedValue(
                value=ast.Name(
                    id=parametrized_name, 
                    ctx=ast.Load()),
                conversion=-1)
        else:
            replace_node = ast.Name(parametrized_name)
        CloneASTUtilities.replace_node(self.nodes[0], self.parent_nodes[0], replace_node)
