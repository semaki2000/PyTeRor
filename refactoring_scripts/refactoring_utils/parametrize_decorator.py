import ast;
class ParametrizeDecorator:
    """Class which holds data for and creates a parametrize decorator."""
    def __init__(self, n_clones:int) -> None:
        self.argnames = [] #str list of argnames
        
        #list with one inner dict per clone, each dict having argnames as keys, with paramvalues as values 
        self.argvals = [{} for _ in range(n_clones)] 

    def is_empty(self):
        return self.argnames == []
    
    def get_values(self, argname:str):
        """Returns a list with lists of values for the given argname. One inner list per clone."""
        values = []
        for clone_dict in self.argvals:
            values.append(clone_dict[argname])
        return values

    def add_argname(self, argname:str):
        self.argnames.append(argname)
        print("adding argname to param dec:", argname)
        for clone_dict in self.argvals:
            clone_dict[argname] = []

        

    def add_value(self, clone_ind:int, argname:str, val):
        """Takes an argname and a list of values for that argname, adding the value at each index to the clone dict at each index.
        """
        assert argname in self.argnames, "Error: an unrecognized argument name has been provided to the parametrize decorator: " + argname
        
        self.argvals[clone_ind][argname].append(val)


    def parse_decorator(self, ast_node):
        """Parses a decorator AST node, storing the names and values. 
        Used for clones when they are being processed.
        Not used for the creation of the parametrize decorator for the target."""
        

        param_names = ast_node.args[0].value.split(",")
        for name in param_names:
            self.add_argname(name)

        for args in ast_node.args[1].elts:
            if type(args) == ast.Tuple:
                [self.add_value(0, param_names[args.index(val)], val) for val in args]

            elif type(args) == ast.Constant:
                self.add_value(0, param_names[0], args) #we can assume there is only one param_name
        self.print_vals()

    def print_vals(self):
        print("printing param decorator:")
        for clone in self.argvals:
            for key in clone.keys():
                print("key:",key)
                for val in clone[key]:
                    if type(val) == ast.Constant:
                        print("\t", val.value)
                    elif type(val) == ast.Name:
                        print("\t", val.id)
            print()
        print("----")
        


