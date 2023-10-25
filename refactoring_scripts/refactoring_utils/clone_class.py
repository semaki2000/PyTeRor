
from .name_generator import NameGenerator;
from .clone_ast_utilities import CloneASTUtilities
from .clone import Clone
from .target_clone import TargetClone
from .node_difference import NodeDifference
from .constant_node_difference import ConstantNodeDifference
from .name_node_difference import NameNodeDifference
from .parametrized_arg import ParametrizedArg

import ast
import sys


class CloneClass():
    """This class keeps track of and refactors a single class of type2 clones, here at the fixed granularity of functions. 
        Clone class therefore here meaning a set of functions which are type2 clones with each other."""
    
    cnt = 0
    def __init__(self, clones : list) -> None:
        """This class keeps track of and refactors a single class of type2 clones, here at the fixed granularity of functions. 
        Clone class therefore here meaning a set of functions which are type2 clones with each other.
    
        Parameters: 
            - clones - list of Clone objects

        """
        self.id = self.cnt
        self.cnt += 1
        self.redundant_clones = []
        self.node_differences = []
        self.node_differences_in_parametrize = [] #boolean list #TODO: change variable name(s)
        self.name_gen = NameGenerator()
        self.clones = clones
        self.process_clones()
        #self.print_pre_info()
        #set target clone
        self.clones[0] = self.target = TargetClone(clone_to_copy=self.clones[0])


    def process_clones(self):
        """Processes the given clones by 
            1. excluding clones which are fixtures (parametrising fixtures will unintentionally parametrize the tests using those fixtures)
        """
        remove_on_index = []
        for clone in self.clones:  
            if clone.is_fixture:
                remove_on_index.insert(0, clone)
            print("paramvals:", clone.parametrized_args)

        for remove_clone in remove_on_index:
            self.clones.remove(remove_clone)



    def print_pre_info(self):
        """Print info before refactoring. On object creation."""
        print(f"Created clone class {self.id} with contents:")
        [print(f"   Function {x.funcname}") for x in self.clones]

    
    def get_ast_node_for_pytest_decorator(self):
        """Creates and returns a @pytest.mark.parametrize AST decorator-node 
        using info from ParametrizedArg objects.
        https://docs.pytest.org/en/7.3.x/how-to/parametrize.html 
        Doesn't yet take into account preexisting parametrization, 
        adding preexisting f_params to the f_params list, 
        or combining the tuples of a_params with preexisting ones.

        Returns:
            An ast.Call node containing a pytest.mark.parametrize decorator, to be put into ast.FunctionDef.decorator_list
        """

        tuple_count = len(self.target.new_parametrized_args[0].values)
        
        f_params = []
        a_params = [[] for x in range(tuple_count)]
        for pdarg in self.target.new_parametrized_args:
            f_params.append(pdarg.argname)
            for ind in range(tuple_count):
                a_params[ind].append(pdarg.values[ind])
        args = []
        args.append(ast.Constant(value=", ".join(f_params)))
        
        list_tuples = []
        for tup in a_params:
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


    def get_clone_differences(self):
        """Travels recursively down through the AST, looking for nodes that are different.
        When a difference is found, a NodeDifference object is created and added to self.nodeDifferences.
        """
        def get_differences_recursive(parent_nodes: list):
            #starts at clone nodes, works its way down AST
            #saves info on whether potential differences are on left side of an assign statement
            
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

                    
                    if type(child_nodes[0]) == ast.Constant:
                        if any(child.value != child_nodes[0].value for child in child_nodes):
                            self.node_differences.append(ConstantNodeDifference(child_nodes, parent_nodes))
                            continue

                    elif type(child_nodes[0]) == ast.Name and any(child.id != child_nodes[0].id for child in child_nodes):
                        
                        self.node_differences.append(NameNodeDifference(child_nodes, parent_nodes))
                        continue
                    
                    #for Attribute (value.attr), only check attr, not value (value should be checked recursively later)
                    elif type(child_nodes[0] == ast.Attribute and any(child.attr != child_nodes[0].attr for child in child_nodes)):
                        

                        #do nothing, maybe add this in as option later                    
                        if False:
                            self.node_differences.append(NodeDifference(child_nodes))
                            continue
                            replace_node = ast.Name(self.name_gen.new_name("attr"))
                            CloneASTUtilities.replace_node(child_nodes[0], parent_nodes[0], replace_node)

                    get_differences_recursive(child_nodes)
                except StopIteration:
                    break
            return
        get_differences_recursive([clone.ast_node for clone in self.clones])

    def extract_clone_differences(self):
        """Uses the NodeDifference objects in the self.nodeDifferences list to extract the differences from each clone, 
        and replace them in the target with the correct name. 
        If two node differences have the same nodes(nodes with the same values), gives them the same name.
        Also looks for the names in       
        """
        #str representation of list of nodes -> generated name for that list of nodes
        nodes_to_name_dict : dict = {}

        #extract nodes marked ._to_extract
        extracted_cnt = 0
        for nd in self.node_differences:
            if not nd.to_extract:
                continue
            if str(nd) in nodes_to_name_dict.keys():
                generated_name = nodes_to_name_dict[str(nd)]
                nd.previously_extracted = True
                
            else:
                generated_name = self.name_gen.new_name(nd.stringtype)
                nd.new_name = generated_name
                nodes_to_name_dict[str(nd)] = generated_name

            self.replace_nodes(nd, generated_name)
            extracted_cnt += 1

        

    def replace_nodes(self, nd, generated_name):

        ind = self.node_differences.index(nd)
        if self.node_differences_in_parametrize[ind]:
            #replace name in .parametrize decorator with new generated name
            pass


        nd.replace_nodes(generated_name)



    def find_local_variables(self):
        """For each NodeDifference object, checks whether it is a local definition (method-local), or a usage of a local variable.
        If so, NodeDifference.to_extract is set to False, meaning that the AST node will not be extracted and replaced with a new name.

        For now, we assume definition of local variables is unconditional.
        """
        nodes_to_local_lineno_definition : dict = {}
        #str representation of list of nodes -> earliest local definition (or None)
        #only matters for NameNodeDifference objects (only they can be on left side of assign)


        #find earliest definition of local name
        for nd in self.node_differences:
            #handle local names (don't have to be parametrized)
            if not str(nd) in nodes_to_local_lineno_definition.keys():
                nodes_to_local_lineno_definition[str(nd)] = float('inf')
            if nd.stringtype == "name" and nd.left_side_assign:
                if nodes_to_local_lineno_definition[str(nd)] > nd.lineno:
                    nodes_to_local_lineno_definition[str(nd)] = nd.lineno

        #for nodes where lineno is newer than newest local definition, do not extract name (uses local name instead)
        for nd in self.node_differences:
            if nd.stringtype == "name":
                if nd.left_side_assign or nodes_to_local_lineno_definition[str(nd)] < nd.lineno:
                    nd.to_extract = False


    def match_parametrize_decorator(self):
        """For each parametrize decorator, check if each parameter name is in a NodeDifferences object. 
        If so, adds to bool list node_differences_in_parametrize, which says whether the node_difference at each index is in parametrize decorator."""


        for nd in self.node_differences:
            in_parametrize = False
            if not nd.to_extract:
                continue

            if type(nd) == NameNodeDifference:
                #check if name in pre-existing parametrize decorator
                for i in range(len(self.clones)):
                    if self.clones[i].parametrized_args != [] and any(nd[i].id == x.argname for x in self.clones[i].parametrized_args):
                        in_parametrize = True            
            self.node_differences_in_parametrize.append(in_parametrize)


    def handle_different_nodes(self, nodes):
        print(f"ERROR: Differing types of nodes on line{nodes[0].lineno}:")
        print(nodes)
        sys.exit()


    def remove_redundant_clones(self):
        """Removes clones which have been parametrized from AST (and therefore subsequent output file).
        """
        for clone in self.redundant_clones:
            clone.detach()


    def set_differences_as_paramd_args(self):
        """Goes ("transposed") through the nodes that are marked as different, extracting the name or value that is different from each, 
        creating a list of tuples, where each tuple has actual parameters for the formal parameters given in pytest.mark.parametrize().
        
        """
        for nd in self.node_differences:
            if nd.previously_extracted or not nd.to_extract:
                continue
            paramd_arg = ParametrizedArg(nd.new_name)
            for clone_ind in range(len(self.clones)):
                paramd_arg.add_value(nd[clone_ind]) 
        
            self.target.new_parametrized_args.append(paramd_arg)
        
    

    def print_post_info(self):
        """Print info after refactoring."""
        print(f"Refactored clone class {self.id}")
        [print(f"   Function {x.funcname}") for x in self.clones]
        print("into " + self.target.new_funcname)
        for x, y in [(self.name_gen.constants_cnt, "constants"), (self.name_gen.names_cnt, "names"), (self.name_gen.other_cnt, "other nodes")]:
            print(f"    Parametrized {x} {y}.")


    def refactor_clones(self):
        """Function to refactor clones."""
        #type 2 clones -> need to parametrize
        if len(self.clones) < 2:
            print("Error in clone class {id}: Cannot parametrize one or fewer tests.")
            return
    
        
        clone_nodes = []
        for clone in self.clones:
            clone_nodes.append(clone.ast_node)

        self.get_clone_differences()

        self.find_local_variables()
        self.match_parametrize_decorator()
        self.extract_clone_differences()
        if len(self.node_differences) > 0:

            #create pytest decorator
            self.set_differences_as_paramd_args()
                
            decorator = self.get_ast_node_for_pytest_decorator()

            self.target.add_parameters_to_func_def(self.name_gen.names)
            self.target.add_decorator(decorator)
            self.target.rename_target()

            self.redundant_clones = self.clones[1:]
            self.remove_redundant_clones()

        #self.print_post_info()
        
        
