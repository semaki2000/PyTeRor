from .node_difference import NodeDifference
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