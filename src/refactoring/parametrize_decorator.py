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

    def get_values_on_ind(self, argname:str, ind:int):
        """Returns a list with lists of values for the given argname and index."""

        return self.argvals[ind][argname]
        

    def add_argname(self, argname:str):
        self.argnames.append(argname)
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
        param_names = [name.strip() for name in param_names]
        for name in param_names:
            self.add_argname(name)

        for args in ast_node.args[1].elts:
            if (
                type(args) == ast.Constant 
                or  (type(args) == ast.Tuple and len(param_names) == 1)
                or (type(args) == ast.List and len(param_names) == 1)
            ):
                #special case for tuples, lists which are supplied as arguments to single-param_name decorators
                #TODO: find out whether there are more special cases here.
                self.add_value(0, param_names[0], args) #we can assume there is only one param_name
            
            elif type(args) == ast.Tuple:
                
                for val in args.elts:
                    ind = args.elts.index(val)
                    self.add_value(0, param_names[ind], val)
                #[self.add_value(0, param_names[args.elts.index(val)], val) for val in args.elts]

            

    def print_vals(self):
        print("printing param decorator:")
        for clone in self.argvals:
            print("clone", self.argvals.index(clone))
            for key in clone.keys():
                print("key:",key)
                for val in clone[key]:
                    if type(val) == ast.Constant:
                        print("\tval:", val.value)
                    elif type(val) == ast.Name:
                        print("\tval:", val.id)
            print()
        print("----")
        


