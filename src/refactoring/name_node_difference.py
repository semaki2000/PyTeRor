from .node_difference import NodeDifference
from .clone_ast_utilities import CloneASTUtilities
import ast

class NameNodeDifference(NodeDifference):

    def __init__(self, nodes, parent_nodes, target_index):
        super().__init__(nodes, parent_nodes, target_index)
        self.context = type(nodes[0].ctx)
        self.stringtype = "name"

    
    def name_on_index(self, name:str, index:int):
        """Checks whether a given string is the node of this object
        at the given clone index."""
        return name == self.nodes[index].id


    def replace_nodes(self, parametrized_name):
        replace_node = ast.Name(parametrized_name)
        CloneASTUtilities.replace_node(self.nodes[0], self.parent_nodes[0], replace_node)

    def check_consistency(self, other):
        """Checks the consistency of identifiers between self and other.
        If consistent (all equal identifiers on equal indexes): 
            returns 'consistent'
        If inconsistent (one or more, but not all, equal identifiers on equal indexes):
            returns 'inconsistent'
        If no overlap between identifiers:
            returns 'different'
        """

        diffs = 0
        index = 0
        while index != len(self.nodes):
            if not self.name_on_index(other.nodes[index].id, index):
                diffs += 1
            index += 1

        if diffs == index:
            return "different"
        elif diffs == 0:
            return "consistent"
        return "inconsistent"
        
        

    def __hash__(self) -> int:
        return hash(str(self))
    
    def __eq__(self, other):
        if type(other) != NameNodeDifference:
            return False
        if len(self.nodes) != len(other.nodes):
            return False
        for i in range(len(self.nodes)):
            if self[i].id != other[i].id:
                return False
        return True