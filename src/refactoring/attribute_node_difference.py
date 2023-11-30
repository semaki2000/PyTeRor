import ast
from .node_difference import NodeDifference

class AttributeNodeDifference(NodeDifference):
    def __init__(self, nodes, parent_nodes, target_index):
        super().__init__(nodes, parent_nodes, target_index)

    
    def get_variants_dict(self):
        """Goes through nodes and builds up and returns a dict different_nodes,
        For a set of nodes which are either "a.b" or "c.d", the dict will look like this:
        ```
        {"a.b":
            [0, 1, 2, 4],
        "c.d":
            [3, 5]}
        ```
        Where the unparsed string of the node will be the key, and a list of indexes will be the values.
        The list of indexes give information on which nodes in the list have this combination of value and attribute. 
        """
        different_nodes = {}
        for ind in range(len(self.nodes)):
            node = self.nodes[ind]
            unparsed_node = ast.unparse(node)
            if unparsed_node in different_nodes.keys():
                different_nodes[unparsed_node].append(ind)
            else:
                different_nodes[unparsed_node] = [ind]

        return different_nodes
