import ast
import sys
from pathlib import Path
from refactoring_utils.ast_parser import ASTParser
from refactoring_utils.clone_ast_utilities import CloneASTUtilities
from refactoring_utils.clone_class_refactorer import CloneClassRefactorer



#currently with function names from test_files/test_check.py

def main():
    if len(sys.argv) == 1:
        print("Usage: python refactor_clones.py filepath [filepaths...]")
        sys.exit()

    filepaths = get_filepaths(sys.argv[1:])
    asts_dict = {} # filepath -> ast_base (for said filepath)
    for filepath in filepaths:
        asts_dict[filepath] = ASTParser.parse_file_to_AST(filepath)
        
    print(asts_dict.keys())

    clones = get_clones()
    clone_classes = []
    #for each clone class
    for clone_class in clones:

        ast_clone_nodes = [] 
        #for filepath in clone class
        for key in clone_class.keys():
            #get ast_base
            ast_base = asts_dict[key]

            for lineno in clone_class[key]:

                #add clone on lineno in filepath to list of clone objects
                ast_clone_nodes.append(CloneASTUtilities.find_clone_node_in_AST(ast_base, clone_lineno=lineno))

        clone_classes.append(CloneClassRefactorer(ast_clone_nodes))

        

    for clone_class in clone_classes:
        clone_class.refactor_clones()

    


    target_location = Path("../refactored_files").resolve()
    for ast_base in asts_dict.values():
        ASTParser.parse_AST_to_file(ast_base, target_location / (Path(sys.argv[1]).stem + "_refactored.py"))



def get_filepaths(args):
    filepaths = []
    for arg in args:
        new_path = Path(arg)
        if new_path.exists() and new_path.is_file():
            filepaths.append(new_path.resolve())  
        else:
            raise FileNotFoundError(new_path)

    return filepaths

def get_clones():
    """Returns clones in this format
    list of clone classes (matching clones), each clone class is a dict
    DICT: from path to int, (absolute, not relative) filepath object to a list of linenumbers specifying start of clone
    """
    #TODO: actually implement. need info from clone detector
    return [{Path("../test_files/calculator/calculator_type2.py").resolve(): [5, 16]}]




main()