from .node_difference import NodeDifference
import ast

class NameNodeDifference(NodeDifference):

    def __init__(self, nodes, parent_nodes, left_side_assign):
        super().__init__(nodes, parent_nodes)
        self.left_side_assign = left_side_assign
        self.stringtype = "name"
        if self.left_side_assign:
            print("On left side of assign statement", end=", ")
            print("Difference with contents:")
            [print(ast.unparse(x)) for x in self.nodes]
            

    
    def __str__(self):
        ret = []
        for node in self.nodes:
            ret.append(node.id)
        return str(ret)
