import ast
import sys
class Clone():
    """Keeps track of a single clone, including its node in the AST, and the file it came from."""

    def __init__(self, ast_node, parent_node, lineno) -> None:
        self.parametrized_values = None
        self.is_fixture : bool = False
        self.ast_node = ast_node
        self.parent_node = parent_node
        self.lineno = lineno
        self.funcname = ast_node.name
        
        self.parse_decorator_list()
    
    def parse_decorator_list(self):
        """'Parses' decorator list of this function to see if function is a fixture or is parameterized.
        Sets value of self.is_fixture, a boolean telling whether this clone is a fixture (fixtures can be disregarded).
        Also sets value of self.parameterized_values:
            if no pytest.mark.parametrization decorator exists -> None
            if pytest.mark.parametrization decorator exists, a tuple of [0] constants (names of parameters) and [1] tuples of values
        """
        

        for decorator in self.ast_node.decorator_list:
            
            #parametrize call, lots of if-s to avoid errors with other decorators
            if type(decorator) == ast.Call and type(decorator.func) == ast.Attribute:
                #if over mutiple lines for "readability"
                if type(decorator.func.value) == ast.Attribute:
                    if type(decorator.func.value.value) == ast.Name:
                        if decorator.func.value.value.id == "pytest" and decorator.func.value.attr == "mark" and decorator.func.attr == "parametrize":

                            #get contents of p.m.parametrize as actual literals
                            #can be in tuple or single element
                            args_list = []
                            for args in decorator.args[1].elts:
                                if type(args) == ast.Tuple:
                                    tuple_vals = tuple(x.value for x in args.elts)
                                elif type(args) == ast.Constant:        
                                    tuple_vals = tuple([args.value])
                                args_list.append(tuple_vals)


                            self.parametrized_values = (decorator.args[0].value, args_list)
                            self.ast_node.decorator_list.remove(decorator) #remove decorator for parametrize (added again later)
                            return

                #fixture with params (fixture as call)
                elif type(decorator.func.value) == ast.Name and decorator.func.value.id == "pytest" and decorator.func.attr == "fixture":
                    self.is_fixture = True
            #simple fixture (no call, only attribute)
            elif type(decorator) == ast.Attribute and type(decorator.value) == ast.Name and  decorator.value.id == "pytest" and decorator.attr == "fixture":
                self.is_fixture = True            
        
            

    def get_ast_node(self):
        return self.ast_node
    
    def detach(self):
        """Detach this clone's node from the AST."""
        
        self.parent_node.body.remove(self.ast_node)