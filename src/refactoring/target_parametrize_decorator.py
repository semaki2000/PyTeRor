import ast
import itertools

from .clone_ast_utilities import CloneASTUtilities as CAU
from .parametrize_decorator import ParametrizeDecorator
class TargetParametrizeDecorator(ParametrizeDecorator):
    """Subclass of ParametrizeDecorator which has functionality specifically for the target of the refactoring."""

    def __init__(self, n_clones: int, funcnames: list, marks: list) -> None:
        super().__init__(n_clones)
        self.funcnames = funcnames
        self.clone_marks = marks
        self.pre_parametrized = {}

        

    def add_argname(self, argname:str):
        super().add_argname(argname)
        self.pre_parametrized[argname] = False

    def add_value_list(self, argname:str, vals_list):
        """Takes an argname and a list of values for that argname, adding the value at each index to the clone dict at each index.
        """
        assert argname in self.argnames, "Error: an unrecognized argument name has been provided to the parametrize decorator: " + argname
        assert len(self.argvals) == len(vals_list), "Error: amount of values supplied does not correspond to the amount of clones"
        
        for ind in range(len(vals_list)):
            self.argvals[ind][argname].append(vals_list[ind])
        

    def remove_value_list(self, argname:str, vals_list):
        """Takes an argname a list of values for that argname, removing the value at each index from the clone dict at each index.
        Throws an error if the value doesn't exist in the dict."""
        
        assert argname in self.argnames, "Error: trying to remove a value from an unrecognized argument name in the parametrize decorator: " + argname
        assert len(self.argvals) == len(vals_list), "Error: amount of values supplied does not correspond to the amount of clones"
        
        for i in range(len(vals_list)):
            values = self.argvals[i][argname]
            


            for j in range(len(values)):
                value = values[j]
                if type(vals_list[i]) == type(value):
                    if type(value) == ast.Name:
                        if vals_list[i].id == value.id:
                            values.pop(j)
                    elif type(value) == ast.Constant:
                        if vals_list[i].value == value.value:
                            values.pop(j)
    

    def add_values_to_index(self, index, argname, values):
        """Takes an index, an argname and a list of values, adding each of these values to the list in self.argvals[index][argname].
        """
        self.argvals[index][argname].extend(values)
        #print(self.argvals[index][argname])
            
    def add_pre_paramd_values_to_index(self, index, argname, values):
        """Special case of add_values_to_index, for pre_paramd names"""
        self.argvals[index][argname] = values
        self.pre_parametrized[argname] = True
        if argname not in self.argnames:
            self.argnames.append(argname)

    def get_newname_for_parameter(self, parameter_name: str):
        """Given a string parameter_name, finds corresponding ast.Name object in argvals, and returns the key it is stored under.
        
        
        If found, also removes the ast.Name object from the list.
        
        If parameter_name is not found, returns False.
        
        Also sets self.pre_parametrized[argname] to True. This is used later when returning the decorator,
        to ensure that the correct amount of pytest.params calls are created in the decorators AST."""
        
        for ind in range(len(self.argvals)):
            for argname in self.argnames:
                try:

                    node = self.argvals[ind][argname][0] #only need first node
                except:
                    #error, doesnt exist. look for variable name ERROR_ERROR in refactored code
                    node = ast.Name("ERROR_ERROR")
                if not isinstance(node, ast.Name):
                    continue
                if node.id == parameter_name:
                    try:
                        assert len(self.argvals[ind][argname]) == 1 and type(self.argvals[ind][argname][0]) == ast.Name, "Error: resetting non-name values in the target parametrize decorator. Should not happen"
                    except:
                        continue

                    self.argvals[ind][argname] = [] #reset
                    self.pre_parametrized[argname] = True
                    return argname                
        return False
    
 

    def pre_paramd(self, ind):
        #TODO: does this assume either none or all clones have this decorator? is that correct?

        #if pre_parametrized args exist in this decorator
        vals = []
        
        max_len = max([len(self.argvals[ind][self.argnames[i]]) for i in range(len(self.argnames))])
        #loop over indexes
        for i in range(max_len):
            vals_at_i = []

            for argname in self.argnames:
                if i >= len(self.argvals[ind][argname]):
                    continue      
                if self.pre_parametrized[argname]:
                    val = self.argvals[ind][argname][i]
                    vals_at_i.append(val)
            vals.append(vals_at_i)

        return vals


    def get_decorator(self):
        """Creates and returns a @pytest.mark.parametrize AST decorator-node 
        using info from ParametrizedArg objects.
        https://docs.pytest.org/en/7.3.x/how-to/parametrize.html 
        Doesn't yet take into account adding preexisting f_params to the f_params list,
        or combining the tuples of a_params with preexisting ones.

        Returns:
            An ast.Call node containing a pytest.mark.parametrize decorator, to be put into ast.FunctionDef.decorator_list
        """
        args = []
        argnames_ordered = []
        for name in self.argnames:
            if self.pre_parametrized[name]:
                argnames_ordered.append(name)
        for name in self.argnames:
            if not self.pre_parametrized[name]:
                argnames_ordered.append(name)
        args.append(ast.Constant(value=", ".join(argnames_ordered)))
        
        a_params = []
        self.print_vals()
        for ind in range(len(self.argvals)):
            clone_dict = self.argvals[ind]
            param_sets = []
            #line underneath asserts that all non-preparametrized argnames are of equal length
            #we check against index -1, as the last element will never be pre_parametrized (they appear first)
            try:
                
                assert all(self.pre_parametrized[argname] or len(clone_dict[argname]) == len(clone_dict[self.argnames[-1]]) for argname in self.argnames)
            except:
                print("failed assertion check because")
                for argname in self.argnames:
                    print("   argname", argname)
                    print("     ", self.pre_parametrized[argname])
                    print("     ", len(clone_dict[argname]) == len(clone_dict[self.argnames[-1]]))

                #print("with functions:", self.funcnames)
                #self.print_vals()
            
            params_for_single_call = []
            
            pre_paramd_values = self.pre_paramd(ind)
            
            #for i2 in range(len(clone_dict[self.argnames[-1]])):
            #after commenting out last line, everything from here... 
            for argname in self.argnames:
                if not self.pre_parametrized[argname]:
                    #print(clone_dict[argname][0].id)

                    params_for_single_call.append(clone_dict[argname][0]) #i2 -> 0
            param_sets.append(params_for_single_call)
            params_for_single_call = []
            #TO HERE was dedented once
            
            if not pre_paramd_values == []:
                param_sets = [tuple(a + b) for a, b in itertools.product(pre_paramd_values, param_sets)]
                #param_sets = [tuple(a + b) for a, b in itertools.product(param_sets, pre_paramd_values)]
                #we need both, but only either/or is possible...
                #how to solve?



            a_params.append(tuple([ind, param_sets])) 


            #UNDERNEATH: incorrect implementation (we don't want cartesian product)
            #all_vals = []
            #for key in clone_dict.keys():
            #    all_vals.append(clone_dict[key])            
            #a_params.append(tuple([ind, list(itertools.product(*all_vals))])) #itertools used for cartesian product. This is WRONG.
            #what is correct: we want each index to match up. Each tuple is a set of values for a call


        list_tuples = []
        for tup in a_params:
            #each tuple contains: 0. an index (clone index), and 1. a list of tuples of values
            for param_set in tup[1]:
                ind = tup[0]
                kw_list = self.get_kw_list(ind)
                
                list_tuples.append(
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id = "pytest", ctx = ast.Load),
                            attr="param"),
                        args= list(param_set),
                        keywords = kw_list
                    )
                )

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
    
    def get_kw_list(self, ind):
        """For a given clone index, returns a list of ast.keyword objects to be supplied to 
        the pytest.param() call in the pytest.mark.parametrize decorator.
        The keyword list first contains the keyword 'id', which represents the name of the clone test function being refactored at given index.
        Then, if the clone test function had any marks, e.g. '@pytest.mark.example_mark', these are added with the keyword 'marks'.
        If there is only one mark, it is supplied to 'marks' as a single value; otherwise, marks contains a list of a values.
        """

        kw_list = [ast.keyword(
            arg="id", 
            value=ast.Constant(value=self.funcnames[ind]))]
        if self.clone_marks[ind] != []:
            if len(self.clone_marks[ind]) < 2:
                    values = self.clone_marks[ind][0]
            else:
                values = ast.List(elts=self.clone_marks[ind])
            kw_list.append(ast.keyword(
                arg="marks",
                value=values))
            
        return kw_list