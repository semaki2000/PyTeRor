import sys
import os
import shutil
from pathlib import Path
#remove files which aren't test_*py or *_test.py (TODO: also check potential pytest.ini file(or hidden .pytest.ini) for filepaths that could include tests other than tests/) 
# run nicad on remaining files to see if code clones in tests of repo

#TODO: remove this class. First check over and make sure there is nothing useful

def main():
    path = get_path_obj()
    orig_dir_name = str(path.name)
    print(os.getcwd())
    tmp_dir_path = Path(os.getcwd() + "/"+ str(path.name) + "_temp_filestructure")
    try:
        shutil.copytree(str(path), str(tmp_dir_path), ignore=ignore_non_test_py_files)
    except FileExistsError:
        print("remove tmp directory first")
        sys.exit()
    except shutil.Error: #permissions thing
        pass

    path = tmp_dir_path
    #run nicad clone detector to find clones
    print(str(path))
    os.system("nicad6 functions py " + str(path) + "/ type2")

    os.system("cp " + str(path) + "_functions-blind-clones/" + orig_dir_name + "_temp_filestructure_functions-blind-clones-0.00-classes.xml repo_search_results/" + orig_dir_name +"_test_clones.xml")
    os.system("./cleanNicad.sh ")
    os.system("rm -r " + str(path))


#copytree will only copy test files and directories
def ignore_non_test_py_files(dir, files):
    print(dir)
    print(files)
    pdir = Path(dir)
    ignore_files = []
    for file in files:
        
        filepath = Path(dir + "/" + file)
        if filepath.match("*/test_*.py") or filepath.match("*_test.py") or filepath.is_dir():
            pass
        else:
            
            ignore_files.append(file)
    return ignore_files


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