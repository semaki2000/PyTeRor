import ast
import sys
from pathlib import Path
from refactoring_scripts.refactoring_utils.ast_parser import ASTParser
from refactoring_scripts.refactoring_utils.clone_ast_utilities import CloneASTUtilities as CAU
from refactoring_scripts.refactoring_utils.clone_class import CloneClass
from find_codeclone_repos.run_clone_detector import RunCloneDetector
from parse_nicad.nicad_parser import NicadParser



def main():
    if len(sys.argv) == 1:
        print("Usage: python refactor_clones.py filepath [filepaths...]")
        sys.exit()


    #filepaths = get_filepaths(sys.argv[1:])
    path = get_path_obj()
    parser_args = RunCloneDetector.run(path)


    xml_parser = NicadParser(*parser_args)
    clones = xml_parser.parse()
    asts_dict = {} # filepath -> ast_base (for said filepath)
    clone_classes = []
    #for each clone class
    for clone_class in clones:

        ast_clone_nodes = [] 
        #for filepath in clone class
        for filepath in clone_class.keys():
            #get ast_base
            if filepath not in asts_dict:
                asts_dict[filepath] = ASTParser.parse_file_to_AST(filepath)

            ast_base = asts_dict[filepath]
            for lineno in clone_class[filepath]:

                #add clone on lineno in filepath to list of clone objects
                ast_clone_nodes.append(CAU.find_clone_node_in_AST(ast_base, clone_lineno=int(lineno)))
        clone_classes.append(CloneClass(ast_clone_nodes))

        

    for clone_class in clone_classes:
        clone_class.refactor_clones()

    
    target_location = Path("refactored_files/repo_test/").resolve()
    for key in asts_dict.keys():
        print("refactored file:", key)
        ASTParser.parse_AST_to_file(asts_dict[key], target_location / Path(key.stem + "_refactored.py"))


#TODO: maybe use with a -f flag for supplying specific files rather than a dir as arg
def get_filepaths(args):
    filepaths = []
    flags = [] #TODO: fill in flags here
    for arg in args:
        if arg in flags:
            continue
        new_path = Path(arg)
        if new_path.exists() and new_path.is_file():
            filepaths.append(new_path.resolve())  
        else:
            raise FileNotFoundError(new_path)

    return filepaths


def get_path_obj():
        if len(sys.argv) != 2:
            print("Usage: python script.py path_to_repository")
            sys.exit()
        stringPath = sys.argv[1]
        pathObj = Path(stringPath)
        if not pathObj.exists():
            print("Given path does not exist: \n" + stringPath)
            sys.exit()
        elif not pathObj.is_dir():
            print("Given path does not point to a directory: \n" + stringPath)
            sys.exit()
        return pathObj

main()