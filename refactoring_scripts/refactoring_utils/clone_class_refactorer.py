
from .name_generator import NameGenerator;
from .clone_ast_utilities import CloneASTUtilities
from .clone import Clone
import ast
import sys

#TODO 
class CloneClassRefactorer():
    redundant_clones = []
    refactored = False
    different_nodes = []
    func_names = []
    parameterized_constants = 0
    parameterized_other = 0

    

    def __init__(self, ast_clones : list, new_var_name="new_var") -> None:
        """This class keeps track of and refactors a single class of type2 clones, here at the fixed granularity of functions. 
        Clone class therefore here meaning a set of functions which are type2 clones with each other.
    
        Parameters: 
            - ast_clones - list of Clone objects
            - new_var_name (optional) - Name of new variables which are created when differences are lifted out of clone functions.
                Defaults to "new_var", giving names like "new_var_0", "new_var_1".

        """
        self.clones = ast_clones
        self.name_gen = NameGenerator(new_var_name)
        self.process_clones()
        print("Created clone class with contents:")
        [print(f"   Function {x.funcname}") for x in self.clones]


    def process_clones(self):
        """Processes the given clones by 
            1. excluding clones which are fixtures (parameterising fixtures will unintentionally parameterize the tests using those fixtures)
        """
        remove_on_index = []
        for clone in self.clones:
            
            if clone.is_fixture:
                remove_on_index.insert(0, clone)

        for remove_clone in remove_on_index:
            self.clones.remove(remove_clone)

    
    def get_ast_node_for_pytest_decorator(self, f_params: list, a_params_list: list):
        """Creates and returns a @pytest.mark.parametrize AST decorator-node 
        from a list of formal parameters and a list of tuples with actual parameters per call.
        https://docs.pytest.org/en/7.3.x/how-to/parametrize.html 


        Parameters: 
            - f_params - list of strings which are names of formal parameters
            - a_params_list - list of tuples of actual parameters, each tuple being correctly ordered actual parameters for a call to the function

        Returns:
            An ast.Call node containing a pytest.mark.parametrize decorator, to be put into ast.FunctionDef.decorator_list
        """

        base_string = "pytest.mark.parametrize('{}', {})"
        f_params_unpacked = ", ".join(f_params)


        parse_string = base_string.format(f_params_unpacked, a_params_list)
        return ast.parse(parse_string).body[0].value


    def extract_differences(self, clone_nodes : list):
        """Given a list of ast-nodes which are (type2) clones, finds nodes that are different between them
        and replaces those with new variables in the AST, returning the nodes that are different between clones.


        Parameters: 
            - nodes - list of ast-nodes which are clones

        Returns:
            List of nodes which are different between the clones.
        """
        def extract_differences_recursive(parent_nodes: list, in_expr: bool):
            #starts at clone nodes, works its way down AST
            
            iterators =  []
            for node in parent_nodes:
                iterators.append(ast.iter_child_nodes(node))    
            while True:
                try:

                    child_nodes = []
                    child_is_expr = False
                    replace = False
                    replace_node = None
                    for ite in iterators:
                        child_nodes.append(next(ite))
                    
                    #if not all same type:
                    if not all(isinstance(child, type(child_nodes[0])) for child in child_nodes):
                        if (in_expr):
                            #unparse nodes to string, extract to be parameterized and replace with call to eval()
                            self.different_nodes.append(child_nodes)
                            eval_arg = ast.Constant(self.name_gen.new_name())
                            eval_node = CloneASTUtilities.get_eval_call_node(eval_arg)
                            CloneASTUtilities.replace_node(child_nodes[0], parent_nodes[0], eval_node)
                            return
                        else:
                            self.handle_different_nodes(child_nodes)
                            
                    #from here, all are same type
                    elif type(child_nodes[0]) == ast.Expr:
                        child_is_expr = True

                    #constants, but different values
                    elif type(child_nodes[0]) == ast.Constant:
                        self.handle_constants(parent_nodes, child_nodes)
                        

                    elif type(child_nodes[0]) == ast.Name and any(child.id != child_nodes[0].id for child in child_nodes):
                        if type(parent_nodes[0]) == ast.Call:
                            self.different_nodes.append(child_nodes)
                            eval_arg = ast.Constant(self.name_gen.new_name())
                            replace_node = CloneASTUtilities.get_eval_call_node(eval_arg)
                            replace = True
                        #not handling obj.attribute(), only name.Call() currently. TODO
                        #not checking args to look for differences
                        else:

                            pass #do nothing, problem will be fixed by refactoring into one of the functions, 
                            #and deleting the other, thereby "choosing" one of the names

                            
                    extract_differences_recursive(child_nodes, child_is_expr if not in_expr else in_expr)
                    if replace:
                        CloneASTUtilities.replace_node(child_nodes[0], parent_nodes[0], replace_node)
                except StopIteration:
                    break
            return
        extract_differences_recursive(clone_nodes, in_expr=False)

    def handle_different_nodes(self, nodes):
        print(f"ERROR: Differing types of nodes on line{nodes[0].lineno}:")
        print(nodes)
        sys.exit()

    def handle_constants(self, parent_nodes, child_nodes):
        """Handle ast-nodes containing ast.Constant objects. Called from self.extract_differences.

        Parameters:
        - parent_nodes - list of the parent nodes of each ast.Constant object (parent in tree)
        - child_nodes - list of ast.Constant objects
        """
        if not any(child.value != child_nodes[0].value for child in child_nodes):
            return
        #else, differing values
        self.different_nodes.append(child_nodes)

        #for "first" parent, remove constant from the AST, replace with variable
        var_replacement = ast.Name(id=self.name_gen.new_name())
        CloneASTUtilities.replace_node(child_nodes[0], parent_nodes[0], var_replacement)


    def remove_redundant_clones(self):
        if not self.refactored:
            print("Cannot remove redundant nodes before refactoring AST")
            sys.exit()
        for clone in self.redundant_clones:
            clone.detach()

    def get_differences_as_args(self):
        """Goes ("transposed") through the nodes that are marked as different, extracting the name or value that is different from each, 
        creating a list of tuples, where each tuple has actual parameters for the formal parameters given in pytest.mark.parametrize().
        
        """
        values = []
        
        for clone_ind in range(len(self.different_nodes[0])):
            cur_nodes_values = []

            for node_list in self.different_nodes:

                if type(node_list[clone_ind]) == ast.Constant:
                    cur_nodes_values.append(node_list[clone_ind].value)
                    self.parameterized_constants += 1

                elif type(node_list[clone_ind]) == ast.Name:
                    cur_nodes_values.append(node_list[clone_ind].id)
                    self.parameterized_other += 1

            values.append(tuple(cur_nodes_values))
                    
        return values


    def refactor_clones(self):
        """Function to refactor clones."""
        #type 2 clones -> need to parametrize
        clone_nodes = []
        for clone in self.clones:
            clone_nodes.append(clone.ast_node)

        self.extract_differences(clone_nodes)
        
        #create pytest decorator
        values = self.get_differences_as_args()
            

        decorator = self.get_ast_node_for_pytest_decorator(self.name_gen.names, values)

        self.clones[0].add_parameters_to_func_def(self.name_gen.names)
        self.clones[0].ast_node.decorator_list.insert(0, decorator)
        self.redundant_clones = self.clones[1:]
        self.refactored = True
        self.remove_redundant_clones()