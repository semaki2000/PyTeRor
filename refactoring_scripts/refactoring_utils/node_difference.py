import ast
from .clone_ast_utilities import CloneASTUtilities

class NodeDifference:
    def __init__(self, nodes, parent_nodes):
        self.nodes = nodes
        self.parent_nodes = parent_nodes

    def __getitem__(self, index : int):
        if 0 <= index and index < len(self.nodes):
            return self.nodes[index]
        raise IndexError("List index out of range")

    def __len__(self):
        return len(self.nodes)

    @property
    def string_type(self):
        pass

    def replace_nodes(self, name_generator):
        replace_node = ast.Name(name_generator.new_name(self.stringType))
        CloneASTUtilities.replace_node(self.nodes[0], self.parent_nodes[0], replace_node)

