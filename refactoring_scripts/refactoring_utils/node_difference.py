import ast
from .clone_ast_utilities import CloneASTUtilities

class NodeDifference:
    def __init__(self, nodes, parent_nodes):
        self.nodes = nodes
        self.parent_nodes = parent_nodes
        self.stringtype = ""
        self.lineno = nodes[0].lineno
        self.to_extract = True

    def __getitem__(self, index : int):
        if 0 <= index and index < len(self.nodes):
            return self.nodes[index]
        raise IndexError("List index out of range")

    def __len__(self):
        return len(self.nodes)
    

    def replace_nodes(self, parametrized_name):
        replace_node = ast.Name(parametrized_name)
        CloneASTUtilities.replace_node(self.nodes[0], self.parent_nodes[0], replace_node)

