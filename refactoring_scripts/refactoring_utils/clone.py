class Clone():
    """Keeps track of a single clone, including its node in the AST, and the file it came from."""

    def __init__(self, ast_node, parent_node, lineno) -> None:
        self.ast_node = ast_node
        self.parent_node = parent_node
        self.lineno = lineno
    
    def get_ast_node(self):
        return self.ast_node
    
    def detach(self):
        """Detach this clone's node from the AST."""
        print(self.parent_node.body)
        self.parent_node.body.remove(self.ast_node)