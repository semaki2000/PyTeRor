from .clone import Clone
import ast

#uses the same ast_object as the first clone in clone_class' list of clones

class TargetClone(Clone):
    """Subclass of clone. Target of parametrization refactoring. Includes methods specific for parametrizing based on differences in the clone class."""
    def __init__(self, clone_to_copy : Clone): 
        super().__init__(clone_to_copy.ast_node, clone_to_copy.parent_node, clone_to_copy.lineno)
        self.new_funcname = self.funcname + "_parametrized"

    def add_parameters_to_func_def(self, param_names: list):
        """Adds given parameter names to the function definition, 
        putting them behind the pre-existing parameters.


        Parameters: 
            - param_names - list of strings to add as parameters to function definition

        Returns:
            None    
        """

        for name in param_names:
            self.ast_node.args.args.append(ast.arg(arg = name))

    def rename_target(self):
        self.ast_node.name = self.new_funcname

    def add_decorator(self, decorator):
        self.ast_node.decorator_list.insert(0, decorator)
