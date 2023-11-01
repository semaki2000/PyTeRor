import ast
import sys
from pathlib import Path
from refactoring_utils.ast_parser import ASTParser
from refactoring_utils.clone_ast_utilities import CloneASTUtilities as CAU
from refactoring_utils.clone_class import CloneClass





def main():
    if len(sys.argv) == 1:
        print("Usage: python refactor_clones.py filepath [filepaths...]")
        sys.exit()

    filepaths = get_filepaths(sys.argv[1:])
    asts_dict = {} # filepath -> ast_base (for said filepath)
    for filepath in filepaths:
        asts_dict[filepath] = ASTParser.parse_file_to_AST(filepath)


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
                ast_clone_nodes.append(CAU.find_clone_node_in_AST(ast_base, clone_lineno=lineno))

        clone_classes.append(CloneClass(ast_clone_nodes))

        

    for clone_class in clone_classes:
        
        clone_class.refactor_clones()

    


    target_location = Path("../refactored_files").resolve()
    for key in asts_dict.keys():
        print("refactored file:", key)
        ASTParser.parse_AST_to_file(asts_dict[key], target_location / (Path(sys.argv[1]).stem + "_refactored.py"))



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
    #return [{Path("../test_files/calculator/calculator_type2.py").resolve(): [5, 16]}]
    #return [{Path("../test_files/funcname_test.py").resolve(): [2, 6, 11, 16]}]
    #return [{Path("../test_files/test_lark_parser.py").resolve(): [164, 264, 279, 200, 295, 327, 311]}]
    #return [{Path("../test_files/ert/test_analysis_config.py").resolve(): [169, 180]},
            #{Path("../test_files/ert/test_analysis_config.py").resolve(): [191, 210]},
            #{Path("../test_files/ert/test_analysis_config.py").resolve(): [198, 217]}]
    return [{Path("../test_files/ert/test_field.py").resolve(): [14, 22, 30]}]



main()