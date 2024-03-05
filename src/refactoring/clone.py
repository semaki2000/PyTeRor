import ast
import fnmatch
from .decorator_checker import DecoratorChecker
from .parametrize_decorator import ParametrizeDecorator
from .parametrize_decorator import parse_argnames_and_argvals
class Clone():
    """Keeps track of a single clone, including its node in the AST, and the file it came from."""

    def __init__(self, ast_node, parent_node, lineno, filehandler) -> None:
        self.ast_node = ast_node
        self.parent_node = parent_node
        self.lineno = lineno
        self.funcname = ast_node.name
        self.filehandler = filehandler

        self.bad_parametrize_decorator = False #True if a decorator has a func call or name instead of values.
        self.is_fixture : bool = False
        self.unknown_decorators_list = []

        self.param_decorator = ParametrizeDecorator(1)
        self.param_dec_nodes = []
        self.marks = [] #list of nodes that are 'pytest.mark's. (Except mark.parametrize)
        
        
        self.target = False
        self.detached = False
        self.refactored = False
        self.filehandler.add_clone(self)
        self.docstring = None

        #only used by target
        self.target_marks = []
        self.new_funcname = self.funcname + "_parametrized"
        
        self.parse_decorator_list()

    #only used by target
    def add_parameters_to_func_def(self, param_names: list):
        """Adds given parameter names to the function definition, 
        putting them behind the pre-existing parameters.

        Parameters: 
            - param_names - list of strings to add as parameters to function definition

        Returns:
            None    
        """

        # get ind after last non keyword-optional argument 
        # (so that we don't accidentally insert parameter before 'self', or after keywords)

        ind = len(self.ast_node.args.args) - len(self.ast_node.args.defaults)

        for name in param_names:
            self.ast_node.args.args.insert(ind, ast.arg(arg = name))
            ind += 1

    #only used by target
    def remove_parameter_from_func_def(self, param_name):
        for ind in range(len(self.ast_node.args.args)):
            node = self.ast_node.args.args[ind]
            if node.arg == param_name:
                self.ast_node.args.args.remove(node)
                return


    #only used by target
    def add_marks(self):
        for mark in self.target_marks:
            self.ast_node.decorator_list.append(mark)

    #only used by target
    def set_common_marks(self, target_marks):
        self.target_marks = target_marks


    #only used by target
    def rename_target(self):
        self.ast_node.name = self.new_funcname

    #only used by target
    def add_decorator(self, decorator):
        self.ast_node.decorator_list.append(decorator)

    #only used by target
    def add_docstring(self, docstring : str):
        docstring_node = ast.Expr(value=ast.Constant(value=docstring))
        self.ast_node.body.insert(0, docstring_node)


    def parse_decorator_list(self):
        """'Parses' decorator list of this function to see if function is a fixture or is parameterized.
        Sets value of self.is_fixture, a boolean telling whether this clone is a fixture (fixtures can be disregarded).
        Also sets value of self.parameterized_values:
            if no pytest.mark.parametrization decorator exists -> None
            if pytest.mark.parametrization decorator exists, a tuple of [0] constants (names of parameters) and [1] tuples of values
        """
        
        to_remove = []
        for decorator in self.ast_node.decorator_list:
            unknown_decorator = False
            if DecoratorChecker.is_parametrize_decorator(decorator):
                #get contents of parametrize marker as actual literals
                
                argnames_kw = False
                argvalues_kw = False
                for kw in decorator.keywords:
                    if kw.arg == "argnames":
                        argnames_kw = True
                        argnames = kw.value
                    elif kw.arg == "argvalues":
                        argvalues_kw = True
                        argvalues = kw.value

                if not argnames_kw:
                    argnames = decorator.args[0]
        

                #argnames can be anything, but for us, SHOULD be string.
                if type(argnames) != ast.Constant or type(argnames.value) != str:
                    unknown_decorator = True
                else:
                    #correctly formed argnames. If it isn't string, we don't bother.
                    argnames = argnames.value

                # argvalues can be as name, or a list of either tuples or single elements.
                if argnames_kw and not argvalues_kw:
                    argvalues = decorator.args[0]
                elif not argnames_kw and not argvalues_kw:
                    argvalues = decorator.args[1]

                if not unknown_decorator and type(argvalues) != ast.List:
                    #print("Error: refactoring program does not currently handle anything other than List as second arg to parametrize decorator")
                    #sys.exit()
                    
                    #set to unknown decorator, this clone will be ignored
                    unknown_decorator = True                


                if not unknown_decorator:
                    self.param_decorator = parse_argnames_and_argvals(argnames, argvalues) + self.param_decorator
                    self.param_dec_nodes.append(decorator)
                    to_remove.append(decorator)

            elif DecoratorChecker.is_fixture_decorator(decorator):
                self.is_fixture = True
            
            elif DecoratorChecker.is_mark_decorator(decorator):
                self.marks.append(decorator)
                #print(decorator.attr if isinstance(decorator, ast.Attribute) else decorator.func.attr)
                to_remove.append(decorator)                                

            elif DecoratorChecker.is_any_pytest_decorator(decorator):
                pass
                #TODO check the actual cases for this... is it necessary? Does it cause extra bugs (f.ex. with pytest plugins probably)
            else:
                unknown_decorator = True
            
            if unknown_decorator:

                self.unknown_decorators_list.append(ast.unparse(decorator))
        
        for decorator in to_remove:
            self.ast_node.decorator_list.remove(decorator)
                
    #TODO: if implementing reading pytest.ini for overriding test name, implement it here too.
    def is_test(self):
        pattern = 'test_*'
        return fnmatch.fnmatch(self.funcname, pattern)

    #TODO: if implementing reading pytest.ini for overriding test class name, implement it here too.    
    def has_bad_parent(self):
        """If the clone is in a class which is not named after pytest test doscpvery rules, return True.
        Else, return False"""
        if self.parent_is_class():
            pattern = 'Test*'
            return not fnmatch.fnmatch(self.parent_node.name, pattern)

        return False

    def remove_multiline_comment(self):
        """This function checks if the first statement in the function body is a docstring.
        If so, sets clone.docstring as this statement, and removes it from function body.
        The statement is removed from the function body because Nicad, the clone detector, ignores docstrings
        when finding clones. This means that two clones that are otherwise the same, 
        can have a difference where one starts with a docstring, and another does not."""
        
        first_line_body = self.filehandler.get_line(self.ast_node.lineno+1).strip()
        if first_line_body[0:3] == '"""' and self.docstring == None:
            self.docstring = self.ast_node.body.pop(0)
            
    def get_param_names(self):
        return self.ast_node.args.args
    
    def name_is_parametrized(self, name_str):
        return name_str in self.param_decorator.argnames

    def name_is_fixture(self, name_str):
        """If name is not in param decorator, it follows that it must be a fixture (if valid pytest test code)"""
        return not self.name_is_parametrized(name_str)

    def get_ast_node(self):
        return self.ast_node
    
    def detach(self):
        """Detach this clone's node from the AST."""
        self.detached = True
        self.parent_node.body.remove(self.ast_node)

    def parent_is_class(self):
        return isinstance(self.parent_node, ast.ClassDef)