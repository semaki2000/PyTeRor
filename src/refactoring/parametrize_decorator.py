import ast;
class ParametrizeDecorator:
    """Class which holds data for and creates a parametrize decorator."""
    def __init__(self, n_clones:int) -> None:
        self.argnames = [] #str list of argnames
        #each argname should be unique, otherwise pytest gives a ValueError: duplicate parametrization
        #as every clone can have multiple decorators, we link each argname to a decorator index
        
        #list with one inner dict per clone, each dict having argnames as keys, with paramvalues as values

        self.n_clones = n_clones
        self.argvals = [{} for _ in range(n_clones)] 
        self.decorators_parsed = 0


    def __len__(self):
        if len(self.argnames) == 0:
            return 0
        #otherwise, len of any dict-value in argvals should do it
        return len(self.argvals[0][self.argnames[0]])
    

    def __add__(self, other):
        """Example:
        arg1: n1 original arguments
        arg2: n2 original arguments
        ```python
        n1 = len(arg1)
        n2 = len(arg2)
        ```
        arg1 * n2, so that arg1 repeats n2 times. 
        E.g: [1, 2, 3, 1, 2, 3]
        For each arg in arg2, arg * n1, 
        so that each arg in repeated n1 times in a row. 
        E.g.["a", "a", "a", "b", "b", "b"]

        This then creates a single parametrize decorator:
        ```python
        @pytest.mark.parametrize("arg1, arg2", [ 
            (1, "a"),
            (2, "a"),
            (3, "a"),
            (1, "b"),
            (2, "b"),
            (3, "b")
            ]
        )
        ```
        """

        print("TRYING TO COMBINE")
        self.print_vals()

        other.print_vals()
        if not isinstance(other, ParametrizeDecorator):
            raise TypeError(f"Unsupported operand type: {type(other)}")
        elif len(self.argvals) > 1 or len(other.argvals) > 1:
            raise ValueError("Cannot add parametrize decorators belonging to more than one clone")
        elif len(self) < 1:
            return other
        elif len(other) == 0:
            return self
        len_this = len(self)
        len_other = len(other)

        this_clone_dict = self.argvals[0]
        other_clone_dict = other.argvals[0]

        for arg in self.argnames:
            #each list of args should repeat len(other) times in a row.
 
            this_clone_dict[arg] = this_clone_dict[arg] * len_other
        
        for arg in other.argnames:
            self.add_argname(arg)
            #For each arg in other, arg * len(self),
            #so that each arg in repeated len(self) times in a row. 
            for val in other_clone_dict[arg]:
                this_clone_dict[arg].extend([val] * len_this)

        print("COMBINED INTO")
        self.print_vals()        
        return self
        



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
            

    def print_vals(self):
        print("printing param decorator:")
        print("with len", len(self))
        for clone in self.argvals:
            print("clone", self.argvals.index(clone))
            for key in clone.keys():
                print("key:",key)
                for val in clone[key]:
                    if type(val) == ast.Constant:
                        print("\tval:", val.value)
                    elif type(val) == ast.Name:
                        print("\tval:", val.id)
                    else:
                        print("\tval:", ast.unparse(val))
            print()
        print("----")
        


def parse_decorator(ast_node) -> ParametrizeDecorator:
        """Parses a decorator AST node, storing the names and values. 
        Used for clones when they are being processed.
        Not used for the creation of the parametrize decorator for the target."""
        
    
        #find n1, len of current decorator
        #n2 = current ast_nodes argvals len
        #check docstring in test_multiple_preexising_pm_decs.py
        #for more info
        #maybe convert this into factory method?
        #and override plus operator for parametrize decorators?


        param_names = ast_node.args[0].value.split(",")
        param_names = [name.strip() for name in param_names]
        pd = ParametrizeDecorator(1) #initialize with '1' clone.
        for name in param_names:
            pd.add_argname(name)

        for args in ast_node.args[1].elts:
            if (
                type(args) == ast.Constant 
                or  (type(args) == ast.Tuple and len(param_names) == 1)
                or (type(args) == ast.List and len(param_names) == 1)
            ):
                #special case for tuples, lists which are supplied as arguments to single-param_name decorators
                #TODO: find out whether there are more special cases here.
                pd.add_value(0, param_names[0], args) #we can assume there is only one param_name
            
            elif type(args) == ast.Tuple:
                
                for val in args.elts:
                    ind = args.elts.index(val)
                    pd.add_value(0, param_names[ind], val)
                #[self.add_value(0, param_names[args.elts.index(val)], val) for val in args.elts]

        return pd