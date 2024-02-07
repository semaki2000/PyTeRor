
from .name_generator import NameGenerator;
from .clone_ast_utilities import CloneASTUtilities
from .clone import Clone
from .node_difference import NodeDifference
from .name_node_difference import NameNodeDifference
from .attribute_node_difference import AttributeNodeDifference
from .target_parametrize_decorator import TargetParametrizeDecorator


import ast
import sys


class CloneClass():
    """This class keeps track of and refactors a single class of type2 clones, here at the fixed granularity of functions. 
        Clone class therefore here meaning a set of functions which are type2 clones with each other."""
    
    cnt = 1 #start cnt (for self.id) at 1, as clone class ID starts at 1 in nicad
    
    def __init__(self, clones : list, custom_mark: bool, split_off = None, split_off_ind = None, verbose = False) -> None:
        """This class keeps track of and refactors a single class of type2 clones, here at the fixed granularity of functions. 
        Clone class therefore here meaning a set of functions which are type2 clones with each other.
    
        Parameters: 
            - clones - list of Clone objects
            TODO: add rest

        """
        #set id
        if split_off:
            self.id = split_off.id+"."+str(split_off_ind)

        else:
            self.id = str(CloneClass.cnt)
            CloneClass.cnt += 1
        
        self.verbose = verbose
        self.custom_mark = custom_mark
        self.split_off = split_off
        self.redundant_clones = []
        self.node_differences = []
        self.name_gen = NameGenerator()
        self.clones = clones
        
        if not split_off:
            self.process_clones()

        self.len_clones = len(clones)
        self.param_decorator = TargetParametrizeDecorator(
            n_clones=len(self.clones), 
            funcnames=[clone.funcname for clone in self.clones],
            marks=[clone.marks for clone in self.clones],
            add_custom_mark=custom_mark)
        self.attribute_difference = False
        
        if (self.verbose):
            self.print_pre_info()
        #set target clone
        if len(self.clones) > 0:
            self.target_ind = 0
            self.target = self.clones[self.target_ind]
            self.target.target = True

    def process_clones(self):
        """Processes the given clones by 
            1. excluding clones which are fixtures (parametrising fixtures will unintentionally parametrize the tests using those fixtures)
            2. excluding clones that have parametrize decorators which supply anything other than a string as first argument, 
                or anything other than a tuple or list as a second argument.
        """
        remove_on_index = []
        for clone in self.clones: #TODO: just reversed() this list and remove in for-loop.
            #clone can be none, if defined inside another function. 
            #we remove this clone here, rather than before creating clone class, this is because we want CloneClass.id to correspond to id in xml file
            if clone is None:
                remove_on_index.insert(0, clone)
            elif (not clone.is_test()) or clone.is_fixture or clone.bad_parametrize_decorator:
                remove_on_index.insert(0, clone)
            else:
                clone.remove_multiline_comment()
            

        for remove_clone in remove_on_index:
            self.clones.remove(remove_clone)



    def print_pre_info(self):
        """Print info before refactoring. On object creation."""
        print()
        print(f"Created clone class {self.id} with contents:")
        [print(f"   Function {x.funcname if not x.parent_is_class() else x.parent_node.name + '.' + x.funcname}") for x in self.clones]


    def check_unknown_decorators(self):
        """Checks each clones unknown_decorators_list, 
        splitting the clone class if 2 or more clones have differences between their unknown decorators"""
        split_groups = {}
        for ind in range(len(self.clones)):
            clone = self.clones[ind]
            #clone.unknown_decorators_list.sort() #genius, but wrong.

            split_groups.setdefault(str(clone.unknown_decorators_list), []).append(ind)

        return split_groups.values()


    def check_parent_nodes(self):
        """Checks the parent nodes of each clone, and splitting the clone class if:
            1. 1 or more clones are in the global scope, whilst 1 or more clones are inside a class.
            2. There are clones in different classes."""
        split_groups = {} #dict from ast_node, where each value is a list which has indices of clones that belong in the same class
        for ind in range(len(self.clones)):
            clone = self.clones[ind]
            if clone.parent_is_class():
                #if not in dict, sets value to [], else appends ind to value list
                split_groups.setdefault(clone.parent_node, []).append(ind)
            else:
                #if in "global" scope, not in class
                split_groups.setdefault("global", []).append(ind)

        return split_groups.values()

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
                    
                    if not all(isinstance(child, type(child_nodes[0])) for child in child_nodes):
                        #if not all same type:
                        #special check for mixture of names and constants:
                        if all((isinstance(child, ast.Name) or isinstance(child, ast.Constant)) for child in child_nodes):
                            self.node_differences.append(NodeDifference(child_nodes, parent_nodes, self.target_ind))
                            continue
                        else:
                            print(child_nodes)
                            for node in child_nodes:
                                print(ast.unparse(node))
                                print("Differing types of nodes")
                                sys.exit()
                    
                    elif type(child_nodes[0]) == ast.Constant:
                        if any(child.value != child_nodes[0].value for child in child_nodes):
                            self.node_differences.append(NodeDifference(child_nodes, parent_nodes, self.target_ind))
                            continue

                    elif type(child_nodes[0]) == ast.Name and any(child.id != child_nodes[0].id for child in child_nodes):
                        
                        self.node_differences.append(NameNodeDifference(child_nodes, parent_nodes, self.target_ind))
                        continue

                    
                    #for Attribute (value.attr), only check attr, not value (value should be checked recursively later)
                    elif type(child_nodes[0]) == ast.Attribute and any(child.attr != child_nodes[0].attr for child in child_nodes):
                        
                        self.node_differences.append(AttributeNodeDifference(child_nodes, parent_nodes, self.target_ind))
                        self.attribute_difference = True
                        continue

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

            nd.replace_nodes(generated_name)
            extracted_cnt += 1

    def find_common_parametrize_decorators(self):
        """Looks through the decorator of each clone (if it has one).
        If all clones have the same decorator, it is added to the targets decorator list, without being changed."""

        #if all have the same argnames
        if self.clones[0].param_decorator.argnames != [] and all(clone.param_decorator.argnames == self.clones[0].param_decorator.argnames for clone in self.clones):
            
            #check if values are same
            same_decorator = True
            for argname in self.clones[0].param_decorator.argnames:

                vals = self.clones[0].param_decorator.get_values_on_ind(argname, 0)
                for clone in self.clones:
                    vals_compare = clone.param_decorator.get_values_on_ind(argname, 0)
                    for i in range(len(vals)):
                            #not all values are the same
                            same_decorator = False
                
            if same_decorator:
                #all have same decorator
                #TODO: 
                self.target.ast_node.decorator_list.extend(self.target.param_dec_nodes)

            else:
                #add argnames to parametrized names. Will be replaced with values later
                for argname in self.clones[0].param_decorator.argnames:
                    self.param_decorator.add_argname(argname)
                    for ind in range(len(self.clones)):
                        self.param_decorator.add_value(ind, argname, ast.Name(argname))

        #different argnames should be handled elsewhere, as it should lead to the creation of a NodeDifference object
        #UPDATE: or maybe not? Parametrize decorator is surely stripped before NodeDifference objects are created...


    def find_common_marks(self):
        """Finds pytest.mark decorators which are common between all clones in the class.
        Adds all common marks into the target's list of common marks."""
        #handle mark decorators:
        common_marks = []
        for clone in self.clones:
            for this_mark in clone.marks:
                in_all = True
                str_mark = ast.unparse(this_mark)
                if any(str_mark == ast.unparse(mark) for mark in common_marks):
                    continue
                for clone2 in self.clones:
                    if clone == clone2: continue
                    if not any(str_mark == ast.unparse(mark) for mark in clone2.marks):
                        in_all = False
                        break
                if in_all:
                    common_marks.append(this_mark)
        for common_mark in common_marks:
            for clone in self.clones:
                for mark in clone.marks:
                    if ast.unparse(common_mark) == ast.unparse(mark):
                        clone.marks.remove(mark)
        self.target.set_common_marks(common_marks)


    def split_on_attributes(self):
        """Goes through list of nodeDifferences and looks for AttributeNodeDifference objects.
        If an AttributeDifference is found, 
        splits the clone class into as many classes as there are variants within the AttributeNodeDifference's nodes."""
        #TODO: check all attributes before splitting. 
        # Currently only splits on first AttributeNodeDifference (but will recursively split if more differences are found)
        attributes = [[] for _ in range(len(self.clones))]
        nds = []
        for nd in self.node_differences:
            nds.append(nd)
            if isinstance(nd, AttributeNodeDifference):
                variants = nd.get_variants_dict()
                for attr, inds in variants.items():
                    for ind in inds:
                        attributes[ind].append(attr)
        

        attr_dict = {}
        for ind in range(len(attributes)):
            strvals = str(attributes[ind])
            if strvals in attr_dict.keys():
                attr_dict[strvals].append(ind)
            else:
                attr_dict[strvals] = [ind]
        
        self.split_clone_class(attr_dict.values(), reason = " because of a difference in attributes.")

    def split_clone_class(self, classes, reason = "."):
        """Splits a clone class into n based on parameter classes which has n elements. 
        Each element is a list of indices."""
        
        if (self.verbose):
            print("Splitting clone class into", len(classes), "classes" + reason)

        #make sure target no longer is target
        self.target.target = False

        classes_split = 0
        for cl in classes:
            classes_split += 1
            clones = []
            for ind in cl:
                clones.append(self.clones[ind])

            CloneClass(clones, self.custom_mark, self, classes_split, verbose=self.verbose).refactor_clones()

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
                    


    def remove_redundant_clones(self):
        """Removes clones which have been parametrized from AST (and therefore subsequent output file).
        """
        for clone in self.redundant_clones:
            clone.detach()


    def add_differences_to_param_decorator(self):
        """Adds nodes that are marked as different between clones to the clone classes TargetParametrizeDecorator,
        which holds value for the pytest.mark.parametrize decorator that will be created
        Does not add nodes that are: 
        - marked as previously extracted ('previously extracted' is decided in extract_clone_differences)
        - not marked as to_extract (decided in find_local_variables)
        """
        for nd in self.node_differences:
            if nd.previously_extracted or not nd.to_extract:
                continue
            self.param_decorator.add_argname(nd.new_name) 
            self.param_decorator.add_value_list(nd.new_name, nd.nodes)
            
            #if a name in funcdef args has been extracted, remove it from funcdef args.
            if isinstance(nd, NameNodeDifference):
                for name in self.target.ast_node.args.args:
                    if nd[self.target_ind].id == name.arg:
                        self.target.ast_node.args.args.remove(name)
                     
            
    def add_docstring(self):
        """Adds docstring of each clone to the targets docstring."""
        if any(clone.docstring != None for clone in self.clones):
            docstring = ""
            for clone in self.clones:
                if clone.docstring != None:
                    docstring += clone.funcname + ":\n"
                    docstring += clone.docstring.value.value + "\n"
                else:
                    pass
                    #TODO: do we want to add a docstring saying 'no docstring' for functions that don't have docstrings?
            self.target.add_docstring(docstring)


    def print_post_info(self):
        """Print info after refactoring."""
        print(f"Refactored clone class {self.id}")
        #[print(f"   Function {x.funcname}") for x in self.clones]
        print("  into " + self.target.new_funcname + " in file: " + str(self.target.filehandler.filepath))
        for x, y in [(self.name_gen.constants_cnt, "constants"), (self.name_gen.names_cnt, "names"), (self.name_gen.other_cnt, "other nodes")]:
            print(f"    Parametrized {x} {y}.")


    def replace_names_with_values(self):
        """Function to replace previously parametrized names with their values. Example:
        ```python
        #clone, pre-refactoring:
        @pytest.mark.parametrize('old_name', [('a'), ('b'), ('c')])
        #during refactoring may become:
        @pytest.mark.parametrize('parametrized_name_0', [old_name, ...])
        #after applying this function, it is turned into:
        @pytest.mark.parametrize('parametrized_name_0', [('a', ...), ('b', ...), ('c', ...)])
        """
        removed_param_names = []
        
        for ind in range(self.len_clones):
            clone = self.clones[ind]
            if clone.param_decorator.is_empty():
                continue
            
            #with old argname, get new name for same arg:
            
            for parameter_name in clone.param_decorator.argnames:
                #get new argname. Old name in param_decorator removes itself in called function
                new_argname = self.param_decorator.get_newname_for_parameter(parameter_name)
                if not new_argname:
                    #NOT SURE why this would be false. Think more about it
                    #should probably throw an error.
                    continue

                removed_param_names.append(parameter_name)
                values = clone.param_decorator.get_values(parameter_name)[0]
                self.param_decorator.add_values_to_index(ind, new_argname, values)
        return removed_param_names                

    def refactor_clones(self):
        """Function to refactor clones."""
        #type 2 clones -> need to parametrize
        if len(self.clones) < 2:
            if (self.verbose):
                print(f"Aborted refactoring of clone class {self.id}: Cannot parametrize one or fewer tests.")
            for clone in self.clones:
                #TODO: check what happens with docstrings
                clone.target = False
                if clone.param_dec_nodes != []:
                    clone.ast_node.decorator_list.extend(clone.param_dec_nodes)
            return
    
        #check parent nodes of clones, split if different:
        split_groups = self.check_parent_nodes()
        if len(split_groups) > 1:
            #groups are split and refactored
            self.split_clone_class(split_groups, reason = " because of a difference in scope (class vs global).")
            return

        #check unknown decorators of clones, split if different:
        split_groups = self.check_unknown_decorators()
        if len(split_groups) > 1:
            #groups are split and refactored
            self.split_clone_class(split_groups, reason = " because of a difference in decorators.")
            return

        #print("getting differences")
        self.get_clone_differences()

        #print("checking whether attribute differences")

        if self.attribute_difference:
            #difference in attributes,
            #split class and return
            self.split_on_attributes()
            return
        
        self.find_common_parametrize_decorators()
        self.find_common_marks()
        #print("finding local variables")
        self.find_local_variables()
        #print("extracting differences")
        self.extract_clone_differences()
        
        if len(self.node_differences) > 0:

            #create pytest decorator
            #print("adding diffs to param decorator")

            self.add_differences_to_param_decorator()
            #print("replacing names with values")
            removed_param_names = self.replace_names_with_values()

            decorator = self.param_decorator.get_decorator()

            
            for param in removed_param_names:
                self.target.remove_parameter_from_func_def(param)
               

            self.target.add_parameters_to_func_def(self.param_decorator.argnames)
            self.target.add_decorator(decorator)
            self.target.add_marks()
            self.target.rename_target()
            self.add_docstring()
            
            for clone in self.clones:
                clone.refactored = True
            self.redundant_clones = self.clones[1:]
            self.remove_redundant_clones()

        if (self.verbose):
            self.print_post_info()
        
