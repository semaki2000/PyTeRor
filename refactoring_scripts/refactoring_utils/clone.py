import ast
import sys
class Clone():
    """Keeps track of a single clone, including its node in the AST, and the file it came from."""

    is_parameterized : bool = False
    is_fixture : bool = False
    def __init__(self, ast_node, parent_node, lineno) -> None:
        self.ast_node = ast_node
        self.parent_node = parent_node
        self.lineno = lineno
        self.funcname = ast_node.name
        
        self.check_decorator_list()
    
    def check_decorator_list(self):
        """Checks decorator list of this function to see if function is a fixture or is parameterized.
        Sets values of self.is_fixture and self.is_parameterized, both of which are booleans.
        """

        for decorator in self.ast_node.decorator_list:
            
            #parametrize call, lots of if-s to avoid errors with other decorators
            if type(decorator) == ast.Call and type(decorator.func) == ast.Attribute:
                #if over mutiple lines for "readability"
                if type(decorator.func.value) == ast.Attribute:
                    if type(decorator.func.value.value) == ast.Name:
                        if decorator.func.value.value.id == "pytest" and decorator.func.value.attr == "mark" and decorator.func.attr == "parametrize":
                            self.is_parametrized = True

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


    def add_parameters_to_func_def(self, param_names: list):
        """Adds given parameter names to the function definition, 
        putting them in front of the pre-existing parameters.


        Parameters: 
            - param_names - list of strings to add as parameters to function definition

        Returns:
            None    
        """
        param_names.reverse()
        for name in param_names:
            self.ast_node.args.args.insert(0, ast.arg(arg = name))