
import sys
import argparse
import tempfile
from pathlib import Path
from refactoring_scripts.refactoring_utils.ast_parser import ASTParser
from refactoring_scripts.refactoring_utils.clone_ast_utilities import CloneASTUtilities as CAU
from refactoring_scripts.refactoring_utils.clone_class import CloneClass
from find_codeclone_repos.run_clone_detector import RunCloneDetector
from parse_nicad.nicad_parser import NicadParser
from refactoring_scripts.refactoring_utils.file_handler import FileHandler




asts_dict = {} # filepath -> ast_base (for said filepath)

def main():

    #filepaths = get_filepaths(sys.argv[1:])
    paths = get_path_obj()
    #TODO: add option to use xml file without using nicad

    list_of_clone_class_dicts = []
    for path in paths:
        if path.is_dir():
            #tmp directory, for copying test files into and running clone detector
            #will be deleted automatically after 'with' is done
            with tempfile.TemporaryDirectory() as tmp_path:
                
                parser_args = RunCloneDetector.run(path, tmp_path)
                xml_parser = NicadParser(*parser_args)
                list_of_clone_class_dicts.extend(xml_parser.parse())
        else:
            #xml file
            xml_parser = NicadParser(path)
            list_of_clone_class_dicts.extend(xml_parser.parse())
    
    file_handlers = []
    clone_classes = clone_class_generator(list_of_clone_class_dicts, file_handlers)

    for clone_class in clone_classes:
        clone_class.refactor_clones()
        
    target_location = Path("refactored_files/repo_test/").resolve()
    print()
    for file in file_handlers:
        file.refactor_file(target_location / Path(file.filepath.stem + "_refactored.py"))
        print("refactored file:", file.filepath)
        print("\t-> " + str(target_location / Path(file.filepath.stem + "_refactored.py")))

def clone_class_generator(clones, file_handlers):
    for clone_class in clones:

        ast_clone_nodes = [] 
        #for filepath in clone class
        for filepath, linenumbers in clone_class.items():
            #get ast_base
            if filepath not in asts_dict:
                asts_dict[filepath] = ASTParser.parse_file_to_AST(filepath)

            ast_base = asts_dict[filepath]
            filehandler=FileHandler(filepath, ast_base)
            file_handlers.append(filehandler)
            
            for lineno in linenumbers:

                #add clone on lineno in filepath to list of clone objects
                ast_clone_nodes.append(CAU.find_clone_node_in_AST(ast_base, clone_lineno=int(lineno), filehandler=filehandler))
        yield CloneClass(ast_clone_nodes)

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

def parseargs():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("paths", action="append", help="path(s) to check for code clones")
    #TODO: add new flag for overwriting file vs creating refactored version. which is default?


    args = parser.parse_args()
    return args

def get_path_obj():
    
    args = parseargs()

    ret = []
    paths = args.paths
    for p in paths:
        path = Path(p)
        if not path.exists():
            print("Given path does not exist: \n" + str(path))
            sys.exit()
        elif not (path.is_dir() or path.suffix == ".xml"):
            print("Given path does not point to a directory or XML file: \n" + str(path))
            sys.exit()
        ret.append(path)
    
    return ret

main()