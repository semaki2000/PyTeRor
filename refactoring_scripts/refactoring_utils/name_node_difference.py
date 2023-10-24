from .node_difference import NodeDifference
import ast

#TODO: use ast.Name.ctx!!! instead of self.left_side_assign
#ctx can be Load/Store/Del
class NameNodeDifference(NodeDifference):

    def __init__(self, nodes, parent_nodes, left_side_assign):
        super().__init__(nodes, parent_nodes)
        self.left_side_assign = left_side_assign
        self.stringtype = "name"

        #TODO: change left_side_assign to: type(ctx) == ast.Store            

    
    def __str__(self):
        ret = []
        for node in self.nodes:
            ret.append(node.id)
        return str(ret)
