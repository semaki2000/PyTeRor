import sys
import argparse
import tempfile
from pathlib import Path
from src.refactoring.ast_parser import ASTParser
from src.refactoring.clone_ast_utilities import CloneASTUtilities as CAU
from src.refactoring.clone_class import CloneClass
from src.refactoring.clone import Clone

from src.detect_clones.run_clone_detector import RunCloneDetector
from src.parse_clone_detection_output.parse_nicad.nicad_parser import NicadParser
from src.refactoring.file_handler import FileHandler
from src.detect_clones.parse_init_file import parse_init_file





asts_dict = {} # filepath -> ast_base (for said filepath)

def main():

    #filepaths = get_filepaths(sys.argv[1:])
    args = parseargs()
    paths = get_path_obj(args)
    out_path = False
    if args.output_dir:
        out_path = Path(args.output_dir)
        assert out_path.exists(), "Output path does not exist"
        assert out_path.is_dir(), "Output path does not point to a directory"
    
    if args.cross_file:
        Clone.split_separate_modules = False
        CloneClass.split_separate_modules = False
    if args.rename:
        Clone.rename_new_func = True
    if args.mark:
        CloneClass.custom_mark = True
    if args.verbose:
        CloneClass.verbose = True
    if args.cross_file:
        CloneClass.split_separate_modules = False
        RunCloneDetector.consistent_cross_file = True
    if args.log_clone_detection:
        RunCloneDetector.log_clone_detector_run = True


    list_of_clone_class_dicts = []
    for path in paths:
        if path.is_dir():
            #config = parse_init_file(path)
            config = {}

            #tmp directory, for copying test files into and running clone detector
            #will be deleted automatically after 'with' is done
            with tempfile.TemporaryDirectory() as tmp_path:

                parser_args = RunCloneDetector.run(path, tmp_path, config)

                if args.experiment:
                    ASTParser.count_tests(tmp_path)

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
        
    target_location = Path("refactored_files/check_repo/").resolve()
    if args.dry_run:
        print("Dry run, no files written to.")
    for file in file_handlers:
        if (args.overwrite):
            refactored = file.refactor_file(file.filepath, args.dry_run)
            if refactored:
                print("refactored file:", file.filepath)
                print("\t-> " + str(file.filepath))
        elif (out_path):
            new_path = out_path / Path(file.filepath.stem + "_refactored.py")
            refactored = file.refactor_file(new_path, args.dry_run)
            if refactored:
                print("refactored file:", file.filepath)
                print("\t-> " + str(new_path))
        else:
            renamed_path = file.filepath.parent / Path(file.filepath.stem + "_refactored.py")
            refactored = file.refactor_file(renamed_path, args.dry_run)
            if refactored:
                print("refactored file:", file.filepath)
                print("\t-> " + str(renamed_path))

    if args.verbose:
        print("Parametrized", CloneClass.tests_parametrized)
        print("in", CloneClass.targets_refactored, "targets")

    if args.experiment:
        print("\nExperiment results:")
        print("Total tests in suite:", ASTParser.tests)
        print("Total clone classes in suite:", CloneClass.cnt - 1) #-1 because value is an ID ready to be assigned to 'next' clone class
        print("Total test clones in suite:", Clone.cnt)
        print("Total tests removed due to parametrization:", CloneClass.tests_parametrized - CloneClass.targets_refactored)
        print("Total clone classes parametrized:", CloneClass.targets_refactored)
        

        print("% of tests removed:", (CloneClass.tests_parametrized - CloneClass.targets_refactored) / ASTParser.tests * 100, "%")
        print("% of clones removed:", CloneClass.tests_parametrized / Clone.cnt * 100, "%")




def clone_class_generator(clones, file_handlers):
    for clone_class in clones:

        ast_clone_nodes = [] 
        #for filepath in clone class
        for filepath, linenumbers in clone_class.items():
            #get ast_base
            if filepath not in asts_dict:
                asts_dict[filepath] = ASTParser.parse_file_to_AST(filepath)

            ast_base = asts_dict[filepath]
            
            for handler in file_handlers:
                if handler.filepath == filepath:
                    filehandler= handler
                    break
            else:
                #if break not executed in for        
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
    
    parser.add_argument("paths", 
        action="append", 
        help="path(s) to check for code clones")
    
    #group
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o", "--output-dir",
                        help="Write new files to given directory, rather than in the directories of the old files")
    group.add_argument("-w", "--overwrite", 
                        action='store_true', 
                        help="Overwrite the files that are being parametrized, rather than creating a new file with _parametrized added to filename")
    #----------------------------- group over


    parser.add_argument("-m", "--mark",
                        action='store_true', 
                        help="Add refactored_parametrized mark to each test that has been refactored, for easy testing whether refactoring was successful")
    parser.add_argument("-v", "--verbose",
                        action='store_true', 
                        help="Give more detailed output on what is happening.")

    parser.add_argument("-lc", "--log-clone-detection",
                        action='store_true', 
                        help="Log clone detector.")

    parser.add_argument("-dr", "--dry-run",
                        action='store_true', 
                        help="Run the program without writing to file.")
    
    parser.add_argument("-cf", "--cross-file",
                        action='store_true', 
                        help="""Enable parametrization across files. 
                        This means that clones in separate modules will be attempted parametrized. 
                        No guarantees can be made as to the correctness of the resulting test.""")

    parser.add_argument("-ex", "--experiment",
                        action='store_true', 
                        help="""Enables option for measuring metrics for experiment. 
                        Will count number of tests before refactoring.
                        Will also count number of tests removed through parametrization (not including targets).""")
    
    parser.add_argument("-r", "--rename",
                        action='store_true', 
                        help="""With this option, when parametrizing tests, the target's function name will have '_parametrized' appended to it.""")


    args = parser.parse_args()
    return args

def get_path_obj(args):

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

if __name__ == "__main__":
    main()