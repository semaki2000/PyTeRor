
from .name_generator import NameGenerator;
from .clone import Clone
import ast
import sys

#TODO 
class CloneClassRefactorer():
    redundant_clones = []
    refactored = False
    

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
        print("Created clone class with contents:")
        print(self.clones)
    
    def get_ast_node_for_pytest_decorator(self, f_params: list, a_params_list: list):
        """Creates and returns a @pytest.mark.parametrize AST decorator-node 
        from a list of formal parameters and a list of tuples with actual parameters per call.
        https://docs.pytest.org/en/7.3.x/how-to/parametrize.html 


        Parameters: 
            - f_params - list of strings which are names of formal parameters
            - a_params_list - list of tuples of actual parameters, each tuple being actual parameters for a call to the function

        Returns:
            An ast.Call node containing a pytest.mark.parametrize decorator, to be put into ast.FunctionDef.decorator_list
        """

        base_string = "pytest.mark.parametrize('{}', {})"
        f_params_unpacked = ", ".join(f_params)


        parse_string = base_string.format(f_params_unpacked, a_params_list)
        return ast.parse(parse_string).body[0].value

    def add_parameters_to_func_def(self, func_def: ast.FunctionDef, param_names: list):
        """Adds given parameter names to the function definition, 
        putting them in front of the pre-existing parameters.


        Parameters: 
            - func_def - ast node of function definition
            - param_names - list of strings to add as parameters to function definition

        Returns:
            None    
        """
        param_names.reverse()
        for name in param_names:
            func_def.args.args.insert(0, ast.arg(arg = name))

    def extract_differences(self, clone_nodes : list):
        """Given a list of ast-nodes which are (type2) clones, finds nodes that are different between them
        and replaces those with new variables in the AST, returning the nodes that are different between clones.


        Parameters: 
            - nodes - list of ast-nodes which are clones

        Returns:
            List of nodes which are different between the clones.
        """
        def extract_differences_recursive(clone_nodes: list):
            different_nodes = []
            
            iterators =  []
            for node in clone_nodes:
                iterators.append(ast.iter_child_nodes(node))    
            while True:
                try:
                    childrenNodes = []
                    for ite in iterators:
                        childrenNodes.append(next(ite))
                    
                    #if not all same type:
                    if not all(isinstance(child, type(childrenNodes[0])) for child in childrenNodes):
                        self.handle_different_nodes(childrenNodes)

                    #constants, but different values
                    elif type(childrenNodes[0]) == ast.Constant and any(child.value != childrenNodes[0].value for child in childrenNodes):
                        
                        different_nodes.append(childrenNodes)

                        #for "first" parent, remove constant from the AST, replace with variable
                        stmt1 = clone_nodes[0]
                        var_replacement = ast.Name(id=self.name_gen.new_name())
                        for attribute in stmt1._fields:
                            #if attr is a list, try to find in list
                            if type(getattr(stmt1, attribute)) == list:
                                attr_list = getattr(stmt1, attribute)
                                try: 
                                    ind = attr_list.index(childrenNodes[0])
                                    attr_list.pop(ind)
                                    attr_list.insert(ind, var_replacement)
                                except ValueError:
                                    pass #wrong attr
                            else:
                                #not list, value can simply be overwritten
                                if getattr(stmt1, attribute) == childrenNodes[0]:
                                    setattr(stmt1, attribute, var_replacement) 

                    elif type(childrenNodes[0]) == ast.Name and any(child.id != childrenNodes[0].id for child in childrenNodes):
                        
                        pass #do nothing, problem will be fixed by refactoring into one of the functions, 
                            #and deleting the other, thereby "choosing" one of the names

                    different_nodes += extract_differences_recursive(childrenNodes)
                except StopIteration:
                    break
            return different_nodes
        return extract_differences_recursive(clone_nodes)

    def handle_different_nodes(self, nodes):
        print(f"ERROR: Differing types of nodes on line{nodes[0].lineno}:")
        print(nodes)
        sys.exit()
    
    def remove_redundant_clones(self):
        if not self.refactored:
            print("Cannot remove redundant nodes before refactoring AST")
            sys.exit()
        for clone in self.redundant_clones:
            clone.detach()


    def refactor_clones(self):
        """Function to refactor clones."""
        #type 2 clones -> need to parametrize
        clone_nodes = []
        for clone in self.clones:
            clone_nodes.append(clone.ast_node)

        differing_nodes_list = self.extract_differences(clone_nodes)
        
        #create pytest decorator
        values = []
        for ind in range(len(differing_nodes_list[0])):
            values.append(tuple([l[ind].value for l in differing_nodes_list]))
            

        decorator = self.get_ast_node_for_pytest_decorator(self.name_gen.names, values)

        self.add_parameters_to_func_def(self.clones[0].ast_node, self.name_gen.names)
        self.clones[0].ast_node.decorator_list.insert(0, decorator)
        self.redundant_clones = self.clones[1:]
        self.refactored = True
        self.remove_redundant_clones()