import ast
import itertools

from .parametrize_decorator import ParametrizeDecorator
class TargetParametrizeDecorator(ParametrizeDecorator):
    """Subclass of ParametrizeDecorator which has functionality specifically for the target of the refactoring."""

    def __init__(self, n_clones: int, funcnames: list, marks) -> None:
        super().__init__(n_clones)
        self.funcnames = funcnames
        self.clone_marks = marks
        

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
            
            for val in values:
                print(ast.unparse(val))

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

    def get_argname_for_preparametrized_names(self, values):
        """Given a list of ast.Name values, containing names which were parametrized pre-refactoring, 
        finds the corresponding argname where these are stored and returns it."""
        #TODO: make more general, or more specific.
        
        assert len(values) == len(self.argvals), "Error: amount of values supplied does not correspond to the amount of clones"
        

        for argname in self.argnames:
            correct = True
            for ind in range(len(self.argvals)):
                node = self.argvals[ind][argname][0] #only need first node
                if not isinstance(node, ast.Name):
                    correct = False
                    continue
                if node.id != values[ind].id:
                    correct = False
                    continue
            if correct:
                
                return argname
            
        return False


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
        args.append(ast.Constant(value=", ".join(self.argnames)))
        
        a_params = []
        for ind in range(len(self.argvals)):
            clone_dict = self.argvals[ind]
            all_vals = []
            for key in clone_dict.keys():
                all_vals.append(clone_dict[key])
            a_params.append(tuple([ind, list(itertools.product(*all_vals))]))



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