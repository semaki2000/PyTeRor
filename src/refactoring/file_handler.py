from .clone_ast_utilities import CloneASTUtilities as CAU
from .target_formatter import TargetFormatter

class FileHandler:

    def __init__(self, filepath, ast_base) -> None:
        self.filepath = filepath
        self.ast_base = ast_base
        self.clones = []
        self.lineno_info = [] #lineno info for original file
        self.lineno_to_target_clone =  {} #dict from lineno to target Clone object


    def add_clone(self, clone):
        self.clones.append(clone)
        self.get_linenumber_info(clone)

    def refactor_file(self, dest_filepath, verbose = False):
        """Aims to refactor the file by keeping as much of the original file as possible"""
        if all(not clone.refactored for clone in self.clones):
            return False

        if verbose:
            print(f"Refactoring file: {self.filepath}")
        
        with open(self.filepath, "r") as file:
            lines = file.readlines()
        
        has_target_clone = self.check_target_clones()
        
        
        remove_ind_list = []

        for ind in range(len(self.clones)):
            if not self.clones[ind].refactored:
                continue
        
            (startline, endline) = self.lineno_info[ind]
            if verbose:
                print(f"removing clone starting at line {startline}")
            for line_ind in range(startline-1, endline):
                remove_ind_list.append(line_ind)

            
        remove_ind_list.sort(reverse=True)
        for ind in remove_ind_list:
            lines.pop(ind)
            if ind in self.lineno_to_target_clone.keys():
                if verbose:
                    print("formatting target clone")
                clone = self.lineno_to_target_clone[ind]

                #format
                #if global test function:
                
                tf = TargetFormatter(clone.ast_node, clone.lineno, clone.parent_is_class)
                formatted = tf.format_target()

                for line in reversed(formatted):
                    lines.insert(ind, line)


        if has_target_clone and not self.pytest_import:
            if verbose:
                print("adding 'import pytest")
            lines.insert(0, "import pytest\n")

        with open(dest_filepath, "w+") as dest_file:
            dest_file.writelines(lines)
        return True


    def check_target_clones(self):
        """For each target in this file's clones, adds the linenumber of target as key, with target itself as value, to dict lineno_to_target_clone
        If any target clones exist in file, returns True, else returns False"""
        has_target_clone = False
        
        for ind in range(len(self.clones)):
            
            if self.clones[ind].target:
                has_target_clone = True
                target_start = self.lineno_info[ind][0]
                self.lineno_to_target_clone[target_start] = self.clones[ind]
        return has_target_clone
    
    @property
    def pytest_import(self):
        return CAU.has_import_statement(self.ast_base)

    def get_linenumber_info(self, clone):
        """For a given clone, adds the first and last lineno of the clone 
        (funcdef/first annotation above funcdef, and last statement in body of funcdef).
        ...to lineno_info list for this FileHandler
        """
        first = clone.lineno
        last = clone.ast_node.end_lineno
        for node in CAU.get_all_descendants(clone.ast_node):
            if hasattr(node, "lineno"):
                if first > node.lineno:                    
                    first = node.lineno
                elif last < node.end_lineno:
                    last = node.end_lineno
        
        self.lineno_info.append((first, last))
        #return (clone.lineno, clone.ast_node.body[-1].lineno, len(clone.ast_node.decorator_list))
    
