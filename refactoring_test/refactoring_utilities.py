#module with refactoring utilities

from pathlib import Path;
import ast;
import sys;


#TODO: turn into class

class RefactorAST():
    def __init__(self, filepath, new_var_name="new_var"):
        
        self.ast_base = self.parse_file_to_AST(filepath)
        self.name_gen = NameGenerator(new_var_name)


    def parse_file_to_AST(self, path : str | Path ) -> ast.AST:
        """Takes a filename, checks validity (.py file, and exists) and 
        returns a complete abstract syntax tree (AST) for the file, from the 'ast' module
        
        Parameters: 
            - path - path to relevant file. str or pathlib.Path

        Returns:
            ast.AST - base of the AST for given python file.
        """
        #error handling
        path = Path(path) #gives valueerror if not a path
        if not path.exists():
            raise ValueError("File does not exist: " + str(path))
        elif not path.is_file():
            raise IsADirectoryError("Given path points to a directory: " + path)
        elif not len(path.parts[-1]) > 3 and path.parts[-1][-3:] == ".py":
            raise ValueError("Not a python file: " + path)
        
        #opening file
        with open(path) as f:
            parsed_ast = ast.parse(f.read())
        return parsed_ast


    def parse_AST_to_file(self, filepath: str | Path):
        """Takes an AST and a filepath, and unparses the given AST into the given file.

        Parameters: 
            - ast_base - base of an AST from 'ast' module
            - filepath - path of location to unparse AST. str or pathlib.Path

        Returns:
            None
        """
        path = Path(filepath)    

        string_ast = ast.unparse(self.ast_base)
        with open(path, "w") as file:
            file.write(string_ast)


    #TODO: find clone pairs between files 
    def find_clone_nodes_in_AST(self, clone_names: list):
        """For a single file, finds AST-nodes of functions which are clones based on function name.


        Parameters: 
            - ast_base - base of an AST from 'ast' module
            - clone_names - list of lists of clone pairs in AST, identified by function names

        Returns:
            List of lists of ast-nodes, with all ast-nodes in the same list being clones with each other.
        """

        clone_nodes = []
        flattened_names = [item for subtuple in clone_names for item in subtuple]

        #only for one file
        for i in range(len(self.ast_base.body)):
            node = self.ast_base.body[i]
            if isinstance(node, ast.FunctionDef) and node.name in flattened_names:
                clone_nodes.append(node)

        return self.sort_clones_into_matched_clone_pairs(clone_nodes, clone_names)


    def sort_clones_into_matched_clone_pairs(self, nodes: list, names: list):
        """Given a list of ast-nodes and a list of which functions are clones with each other, sorts ast-nodes into clone-pairs


        Parameters: 
            - nodes - list of ast-nodes which are clones
            - names - list of lists of clone pairs in AST, identified by function names

        Returns:
            List of lists of ast-nodes, with all ast-nodes in the same list being clones with each other.
        """
        #TODO: inefficient
        all_matched_nodes = []
        for sublist in names:

            current_matched = []
            all_matched_nodes.append(current_matched)

            for node in nodes:
                if node.name in sublist:
                    current_matched.append(node)
        return all_matched_nodes


    def find_differences(self, clone_nodes : list):
        """Given a list of ast-nodes which are (type2) clones, finds nodes that are different between them
        and replaces those with new variables in the AST, returning the nodes that are different between clones.


        Parameters: 
            - nodes - list of ast-nodes which are clones

        Returns:
            List of nodes which are different .
        """
        return self.find_differences_recursive(clone_nodes)

    def find_differences_recursive(self, clone_nodes: list):
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
                print(childrenNodes[0])
                if not all(isinstance(child, type(childrenNodes[0])) for child in childrenNodes):
                    print("Differing types in childrenNodes:")
                    print(childrenNodes)
                    sys.exit(1)

                #constants but different values
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

                different_nodes += self.find_differences_recursive(childrenNodes)
            except StopIteration:
                break
        return different_nodes


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


    def detach_redundant_clones(self, redundant_clones: list):
        """Detaches given nodes from the AST.

        Parameters: 
            - redundant_clones - list of ast nodes which are redundant clones 

        Returns:
            None    
        """
        parent = self.ast_base
        


class NameGenerator:
    names = []
    cnt = 0
    def __init__(self, basename: str):
        self.basename = basename

    def new_name(self):
        name = self.basename + "_" + str(self.cnt)
        self.cnt += 1
        self.names.append(name)
        return name