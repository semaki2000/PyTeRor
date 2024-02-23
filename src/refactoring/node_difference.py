import ast
from .clone_ast_utilities import CloneASTUtilities

class NodeDifference:
    def __init__(self, nodes, parent_nodes, target_index):
        self.nodes = nodes
        self.parent_nodes = parent_nodes
        self.target_index = target_index
        self.stringtype = "constant" #we default to constant (because we removed ConstantNodeDifference class, instead implementing it as the superclass)
        self.lineno = nodes[0].lineno
        self.to_extract = True
        self.previously_extracted = False
        self.new_name = ""

    def __getitem__(self, index : int):
        if 0 <= index and index < len(self.nodes):
            return self.nodes[index]
        raise IndexError("List index out of range")

    def __len__(self):
        return len(self.nodes)
    
    def __str__(self):
        ret = []
        for node in self.nodes:
            if isinstance(node, ast.Name):
                ret.append(node.id)
            elif isinstance(node, ast.Constant):
                ret.append(node.value)
            elif isinstance(node, ast.Attribute):
                ret.append(ast.unparse(node))
            else:
                print("Error in NodeDifference. Shouldn't come here.")
        return str(ret)
    
    def in_fstring(self):
        #TODO: could be further down in an fstring
        if type(self.parent_nodes[0]) == ast.JoinedStr:
            return True
        return False

    def replace_nodes(self, parametrized_name):
        if self.in_fstring():
            replace_node = ast.FormattedValue(
                value=ast.Name(
                    id=parametrized_name, 
                    ctx=ast.Load()),
                conversion=-1)
        else:
            replace_node = ast.Name(parametrized_name)
        CloneASTUtilities.replace_node(self.nodes[0], self.parent_nodes[0], replace_node)


