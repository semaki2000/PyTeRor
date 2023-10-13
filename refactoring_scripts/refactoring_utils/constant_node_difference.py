from .node_difference import NodeDifference
import ast

class ConstantNodeDifference(NodeDifference):

    def __init__(self, nodes, parent_nodes):
        super().__init__(nodes, parent_nodes)


    def string_type(self):
        return "name"