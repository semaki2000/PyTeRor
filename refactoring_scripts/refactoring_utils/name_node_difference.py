from .node_difference import NodeDifference
import ast

#TODO: use ast.Name.ctx!!! instead of self.left_side_assign
#ctx can be Load/Store/Del
class NameNodeDifference(NodeDifference):

    def __init__(self, nodes, parent_nodes):
        super().__init__(nodes, parent_nodes)
        self.left_side_assign = type(nodes[0].ctx) == ast.Store
        self.stringtype = "name"

    
    def in_names(self, name:str):
        """Checks whether a given string is one of the nodes of this object"""
        return any(node.id == name for node in self.nodes)
            

    def __str__(self):
        ret = []
        for node in self.nodes:
            ret.append(node.id)
        return str(ret)
