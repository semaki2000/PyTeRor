
from .name_generator import NameGenerator;
from .clone_ast_utilities import CloneASTUtilities
from .clone import Clone
from .target_clone import TargetClone

import ast
import sys


class CloneClass():
    """This class keeps track of and refactors a single class of type2 clones, here at the fixed granularity of functions. 
        Clone class therefore here meaning a set of functions which are type2 clones with each other."""
    

    def __init__(self, ast_clones : list) -> None:
        """This class keeps track of and refactors a single class of type2 clones, here at the fixed granularity of functions. 
        Clone class therefore here meaning a set of functions which are type2 clones with each other.
    
        Parameters: 
            - ast_clones - list of Clone objects

        """
        self.redundant_clones = []
        self.refactored = False
        self.different_nodes = []
        self.func_names = []
        self.name_gen = NameGenerator()
        self.clones = ast_clones
        self.process_clones()
        print("Created clone class with contents:")
        [print(f"   Function {x.funcname}") for x in self.clones]
        #set target clone
        self.clones[0] = self.target = TargetClone(clone_to_copy=self.clones[0])




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
        Also takes into account preexisting parametrization, 
        adding preexisting f_params to the f_params list, 
        and combining the tuples of a_params with preexisting ones.


        Parameters: 
            - f_params - list of strings which are names of formal parameters
            - a_params_list - list of tuples of actual parameters, each tuple being correctly ordered actual parameters for a call to the function

        Returns:
            An ast.Call node containing a pytest.mark.parametrize decorator, to be put into ast.FunctionDef.decorator_list
        """

        args = []
        args.append(ast.Constant(value=", ".join(f_params)))
        
        list_tuples = []
        for tup in a_params_list:
            if len(tup) == 1:
                list_tuples.append(tup[0])
            else:
                list_tuples.append(ast.Tuple(elts = list(tup)))
        args.append(ast.List(elts=list_tuples))
        pytest_node = ast.Call(
            func=ast.Attribute(
                value = ast.Attribute(
                    value = ast.Name(id="pytest"), 
                    attr = "mark"),
                attr = "parametrize"), 
            args = args,
            keywords = [])
                
        return pytest_node


    def extract_differences(self, clone_nodes : list):
        """Given a list of ast-nodes which are (type2) clones, finds nodes that are different between them
        and replaces those with new variables in the AST, returning the nodes that are different between clones.


        Parameters: 
            - nodes - list of ast-nodes which are clones

        Returns:
            List of nodes which are different between the clones.
        """
        def extract_differences_recursive(parent_nodes: list):
            #starts at clone nodes, works its way down AST
            
            iterators =  []
            for node in parent_nodes:
                iterators.append(ast.iter_child_nodes(node))    
            while True:
                try:

                    child_nodes = []
                    
                    for ite in iterators:
                        child_nodes.append(next(ite))
                    
                    #if not all same type, something probably wrong:
                    if not all(isinstance(child, type(child_nodes[0])) for child in child_nodes):
                        self.handle_different_nodes(child_nodes)
        
                    #from here, all are same type

                    #constants, but different values
                    elif type(child_nodes[0]) == ast.Constant:
                        self.handle_constants(parent_nodes, child_nodes)
                        

                    elif type(child_nodes[0]) == ast.Name and any(child.id != child_nodes[0].id for child in child_nodes):
                        
                        self.different_nodes.append(child_nodes)
                        replace_node = ast.Name(self.name_gen.new_name("name"))
                        CloneASTUtilities.replace_node(child_nodes[0], parent_nodes[0], replace_node)
                        
                        #TODO: recognize when names are different, without it having importance. check README 
                    
                    #for Attribute (value.attr), only check attr, not value (value should be checked recursively later)
                    elif type(child_nodes[0] == ast.Attribute and any(child.attr != child_nodes[0].attr for child in child_nodes)):
                        

                        if False:
                            self.different_nodes.append(child_nodes)
                            replace_node = ast.Name(self.name_gen.new_name("attr"))
                            CloneASTUtilities.replace_node(child_nodes[0], parent_nodes[0], replace_node)

                        #do nothing, maybe add this in as option later                    
                    
                    extract_differences_recursive(child_nodes)
                        
                except StopIteration:
                    break
            return
        extract_differences_recursive(clone_nodes)

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
        var_replacement = ast.Name(id=self.name_gen.new_name("constant"))
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
        print(self.different_nodes)
        for clone_ind in range(len(self.different_nodes[0])):
            cur_nodes_values = []

            for node_list in self.different_nodes:

                cur_nodes_values.append(node_list[clone_ind])

            values.append(tuple(cur_nodes_values))

        return values

    def print_info(self):
        print("Refactored")
        [print(f"   Function {x.funcname}") for x in self.clones]
        print("into " + self.target.new_funcname)
        for x, y in [(self.name_gen.constants_cnt, "constants"), (self.name_gen.names_cnt, "names"), (self.name_gen.other_cnt, "other nodes")]:
            print(f"    Parametrized {x} {y}.")


    def refactor_clones(self):
        """Function to refactor clones."""
        #type 2 clones -> need to parametrize
        if len(self.clones) < 2:
            print("Cannot parametrize one or fewer tests.")
            return
    
        #else
        clone_nodes = []
        for clone in self.clones:
            clone_nodes.append(clone.ast_node)

        self.extract_differences(clone_nodes)
        if len(self.different_nodes) > 0:

            #create pytest decorator
            values = self.get_differences_as_args()
                
            decorator = self.get_ast_node_for_pytest_decorator(self.name_gen.names, values)
            self.target.add_parameters_to_func_def(self.name_gen.names)
            self.target.add_decorator(decorator)
            self.redundant_clones = self.clones[1:]
            self.refactored = True
            self.remove_redundant_clones()

        self.print_info()
        
