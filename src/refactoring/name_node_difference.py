from .node_difference import NodeDifference
from .clone_ast_utilities import CloneASTUtilities
import ast

class NameNodeDifference(NodeDifference):

    def __init__(self, nodes, parent_nodes, target_index):
        super().__init__(nodes, parent_nodes, target_index)
        self.context = type(nodes[0].ctx)
        self.stringtype = "name"

    
    def in_names(self, name:str):
        """Checks whether a given string is one of the nodes of this object"""
        return any(node.id == name for node in self.nodes)
            

    def replace_nodes(self, parametrized_name):
        replace_node = ast.Name(parametrized_name)
        CloneASTUtilities.replace_node(self.nodes[0], self.parent_nodes[0], replace_node)