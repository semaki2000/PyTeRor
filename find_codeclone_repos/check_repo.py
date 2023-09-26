import sys
import os
import shutil
from pathlib import Path
#remove files which aren't test_*py or *_test.py (TODO: also check potential pytest.ini file(or hidden .pytest.ini))
# run nicad on remaining files to see if code clones in tests of repo


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
    test_files = [x for x in path.rglob("test_*.py")]
    test_files += [x for x in path.rglob("*_test.py")]
    gen = path.rglob("*")
    while True:
        try:
            next_file = next(gen)
            if not next_file in test_files:
                if next_file.is_file():
                    print("removing file:", next_file)
                    next_file.unlink()
        except StopIteration:
            break

    #run nicad clone detector to find clones
    print(str(path))
    os.system("nicad6 functions py " + str(path) + "/ type2")

    os.system("cat " + str(path) + "_functions-blind-clones/" + orig_dir_name + "_temp_filestructure_functions-blind-clones-0.00-classes.xml > repo_search_results/" + orig_dir_name +"_test_clones.xml")
    
    os.system("./cleanNicad.sh ")
    os.system("rm -r " + str(path))


#copytree will only copy test files and directories
def ignore_non_test_py_files(dir, files):
    print(dir)
    print(files)
    pdir = Path(dir)
    ignore_files = []
    for file in files:
        print("checking file", file)
        filepath = Path(dir + "/" + file)
        if filepath.match("*/test_*.py") or filepath.match("*_test.py") or filepath.is_dir():
            pass
        else:
            print("ignoring", file)
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